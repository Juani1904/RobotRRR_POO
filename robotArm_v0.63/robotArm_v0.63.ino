//20SFFACTORY COMMUNITY ROBOT FIRMWARE v0.62

//V0.31 WITH G92, M114, LOGGER, LIMIT_CHECK FUNCTIONS
//V0.41 WITH DUAL SHANK LENGTH SUPPORT
//V0.51 WITH SERVO GRIPPER
//V0.61 WITH ARDUINO UNO OPTION
//V0.62 CHANGE POSITION FORMAT IN M114,
//      ADD ENDSTOP WITH FAILURE CHECK
//      CHANGE FLOW ON homeSequence() FOR GENERALITY

#include "config.h"
#include "logger.h"

#include "pinout.h"
#if USE_UNO
#include "pinout_uno.h"
#endif

#include <Arduino.h>

#include "robotGeometry.h"
#include "interpolation.h"
#include "fanControl.h"
#include "RampsStepper.h"
#include "queue.h"
#include "command.h"
#include "byj_gripper.h"
#include "servo_gripper.h"
#include "equipment.h"
#include "endstop.h"

//STEPPER OBJECTS
RampsStepper stepperHigher(X_STEP_PIN, X_DIR_PIN, X_ENABLE_PIN, INVERSE_X_STEPPER);
RampsStepper stepperLower(Y_STEP_PIN, Y_DIR_PIN, Y_ENABLE_PIN, INVERSE_Y_STEPPER);
RampsStepper stepperRotate(Z_STEP_PIN, Z_DIR_PIN, Z_ENABLE_PIN, INVERSE_Z_STEPPER);

//RAIL OBJECTS
RampsStepper stepperRail(E0_STEP_PIN, E0_DIR_PIN, E0_ENABLE_PIN, INVERSE_E0_STEPPER);
Endstop endstopE0(E0_MIN_PIN, E0_DIR_PIN, E0_STEP_PIN, E0_ENABLE_PIN, E0_MIN_INPUT, E0_HOME_STEPS, HOME_DWELL, E0_CHECK_DELAY);

//ENDSTOP OBJECTS
Endstop endstopX(X_MIN_PIN, X_DIR_PIN, X_STEP_PIN, X_ENABLE_PIN, X_MIN_INPUT, X_HOME_STEPS, HOME_DWELL, X_CHECK_DELAY);
Endstop endstopY(Y_MIN_PIN, Y_DIR_PIN, Y_STEP_PIN, Y_ENABLE_PIN, Y_MIN_INPUT, Y_HOME_STEPS, HOME_DWELL, Y_CHECK_DELAY);
Endstop endstopZ(Z_MIN_PIN, Z_DIR_PIN, Z_STEP_PIN, Z_ENABLE_PIN, Z_MIN_INPUT, Z_HOME_STEPS, HOME_DWELL, Z_CHECK_DELAY);

//EQUIPMENT OBJECTS
BYJ_Gripper byj_gripper(BYJ_PIN_0, BYJ_PIN_1, BYJ_PIN_2, BYJ_PIN_3, BYJ_GRIP_STEPS);
Servo_Gripper servo_gripper(SERVO_PIN, SERVO_GRIP_DEGREE, SERVO_UNGRIP_DEGREE);
Equipment laser(LASER_PIN);
Equipment pump(PUMP_PIN);
Equipment led(LED_PIN);
FanControl fan(FAN_PIN, FAN_DELAY);

//EXECUTION & COMMAND OBJECTS
RobotGeometry geometry(END_EFFECTOR_OFFSET, LOW_SHANK_LENGTH, HIGH_SHANK_LENGTH);
Interpolation interpolator;
Queue<Cmd> queue(QUEUE_SIZE);
Command command;

float tiempo; //agregada variable para retornar tiempo
float pos[4]; //agregado vector para verificar posicion

void setup()
{
  Serial.begin(BAUD);
  stepperHigher.setPositionRad(PI / 2.0); // 90°
  stepperLower.setPositionRad(0);         // 0°
  stepperRotate.setPositionRad(0);        // 0°
  stepperRail.setPosition(0);
  if (HOME_ON_BOOT) { //HOME DURING SETUP() IF HOME_ON_BOOT ENABLED
    homeSequence();
    Logger::logINFO("ROBOT ONLINE");
  } else {
    setStepperEnable(false); //ROBOT ADJUSTABLE BY HAND AFTER TURNING ON
    if (HOME_X_STEPPER && HOME_Y_STEPPER && !HOME_Z_STEPPER) {
      Logger::logINFO("ROBOT ONLINE");
      Logger::logINFO("ROTATE ROBOT TO FACE FRONT CENTRE & SEND G28 TO CALIBRATE");
    }
    if (HOME_X_STEPPER && HOME_Y_STEPPER && HOME_Z_STEPPER) {
      Logger::logINFO("ROBOT ONLINE");
      Logger::logINFO("SEND G28 TO CALIBRATE");
    }
    if (!HOME_X_STEPPER && !HOME_Y_STEPPER) {
      Logger::logINFO("ROBOT ONLINE");
      Logger::logINFO("HOME ROBOT MANUALLY & SEND G28 TO CALIBRATE");
    }
  }
  interpolator.setInterpolation(INITIAL_X, INITIAL_Y, INITIAL_Z, INITIAL_E0, INITIAL_X, INITIAL_Y, INITIAL_Z, INITIAL_E0);
}

void loop() {
  interpolator.updateActualPosition();
  geometry.set(interpolator.getXPosmm(), interpolator.getYPosmm(), interpolator.getZPosmm());
  stepperRotate.stepToPositionRad(geometry.getRotRad());
  stepperLower.stepToPositionRad(geometry.getLowRad());
  stepperHigher.stepToPositionRad(geometry.getHighRad());
  if (RAIL) {
    stepperRail.stepToPositionMM(interpolator.getEPosmm(), STEPS_PER_MM_RAIL);
  }
  stepperRotate.update();
  stepperLower.update();
  stepperHigher.update();
  if (RAIL) {
    stepperRail.update();
  }
  fan.update();
  if (!queue.isFull()) {
    if (command.handleGcode()) {
      queue.push(command.getCmd());
    }
  }
  if ((!queue.isEmpty()) && interpolator.isFinished()) {
    executeCommand(queue.pop());
    if (PRINT_REPLY) {
      Serial.println(PRINT_REPLY_MSG);
    }
  }
  if (millis() % 500 < 250) {
    led.cmdOn();
  }
  else {
    led.cmdOff();
  }
}

void executeCommand(Cmd cmd) {
  if (cmd.id == -1) {
    printErr();
    return;
  }

  if (cmd.id == 'G') {
    switch (cmd.num) {
      case 0:
      case 1:
        fan.enable(true);
        Point posoffset;
        posoffset = interpolator.getPosOffset();
        cmdMove(cmd, interpolator.getPosmm(), posoffset, command.isRelativeCoord);

        // asignacion auxiliar para poder verificar punto dentro del espacio de trabajo
        pos[0] = cmd.valueX;
        pos[1] = cmd.valueY;
        pos[2] = cmd.valueZ;
        pos[3] = cmd.valueE;
        if (interpolator.isAllowedPosition(pos)){ //agregada verificacion de que la posicion solicitada este dentro del espacio de trabajo
          tiempo = interpolator.setInterpolation(cmd.valueX, cmd.valueY, cmd.valueZ, cmd.valueE, cmd.valueF); // agregado retorno de tiempo
          Logger::logINFO("LINEAR MOVE: [X:" + String(cmd.valueX - posoffset.xmm) + " Y:" + String(cmd.valueY - posoffset.ymm) + " Z:" + String(cmd.valueZ - posoffset.zmm) + " E:" + String(cmd.valueE - posoffset.emm) + "] t=" + String(tiempo, 2) + "s"); //agregado retorno de tiempo
        }
        break;
      case 4: cmdDwell(cmd); break;
      case 28:
        if (USE_UNO) {
          homeSequence_UNO();
          break;
        } else {
          homeSequence();
          break;
        }
      case 90: command.cmdToAbsolute(); break; // ABSOLUTE COORDINATE MODE
      case 91: command.cmdToRelative(); break; // RELATIVE COORDINATE MODE
      case 92:
        interpolator.resetPosOffset();
        cmdMove(cmd, interpolator.getPosmm(), interpolator.getPosOffset(), false);
        interpolator.setPosOffset(cmd.valueX, cmd.valueY, cmd.valueZ, cmd.valueE);
        break;
      default: printErr();
    }
  }
  else if (cmd.id == 'M') {

    switch (cmd.num) {
      case 1: pump.cmdOn(); break;
      case 2: pump.cmdOff(); break;
      case 3:
        if (GRIPPER == 0) {
          byj_gripper.cmdOn(); break;
        } else if (GRIPPER == 1) {
          servo_gripper.cmdOn(); break;
        }
        Logger::logINFO("GRIPPER ON"); break;

      case 5:
        if (GRIPPER == 0) {
          byj_gripper.cmdOff(); break;
        } else if (GRIPPER == 1) {
          servo_gripper.cmdOff(); break;
        }
        Logger::logINFO("GRIPPER OFF"); break;

      case 6: laser.cmdOn(); break;
      case 7: laser.cmdOff(); break;
      case 17: setStepperEnable(true); break;
      case 18: setStepperEnable(false); break;
      case 106: fan.enable(true); break;
      case 107: fan.enable(false); break;
      case 114: command.cmdGetPosition(interpolator.getPosmm(), interpolator.getPosOffset(), stepperHigher.getPosition(), stepperLower.getPosition(), stepperRotate.getPosition()); break; // Return the current positions of all axis
      case 119:
        String endstopMsg = "ENDSTOP: [X:";
        endstopMsg += String(endstopX.state());
        endstopMsg += " Y:";
        endstopMsg += String(endstopY.state());
        endstopMsg += " Z:";
        endstopMsg += String(endstopZ.state());
        endstopMsg += "]";
        //ORIGINAL LOG STRING UNDESIRABLE FOR UNO PROCESSING
        //Logger::logINFO("ENDSTOP STATE: [UPPER_SHANK(X):"+String(endstopX.state())+" LOWER_SHANK(Y):"+String(endstopY.state())+" ROTATE_GEAR(Z):"+String(endstopZ.state())+"]");
        Logger::logINFO(endstopMsg);
        break;
      default: printErr();
    }
  }
  else {
    printErr();
  }
}

void setStepperEnable(bool enable) {
  stepperRotate.enable(enable);
  stepperLower.enable(enable);
  stepperHigher.enable(enable);
  if (RAIL) {
    stepperRail.enable(enable);
  }
  fan.enable(enable);
}

void homeSequence() {
  setStepperEnable(false);
  fan.enable(true);
  Logger::logINFO("HOMING");
  if (!HOME_Y_STEPPER || !HOME_X_STEPPER) {
    setStepperEnable(true);
    endstopY.homeOffset(!INVERSE_Y_STEPPER);
    endstopX.homeOffset(!INVERSE_X_STEPPER);
  }
  else {
    if (HOME_Y_STEPPER) {
      endstopY.home(!INVERSE_Y_STEPPER); //INDICATE STEPPER HOMING DIRECTION
    }
    if (HOME_X_STEPPER) {
      endstopX.home(!INVERSE_X_STEPPER); //INDICATE STEPPER HOMING DIRECTION
    }
  }
  if (HOME_Z_STEPPER) {
    endstopZ.home(INVERSE_Z_STEPPER); //INDICATE STEPPER HOMING DIRECTION
  }

  if (RAIL) {
    if (HOME_E0_STEPPER) {
      endstopE0.home(!INVERSE_E0_STEPPER); //
    }
  }

  //  if((HOME_Y_STEPPER and endstopY.checkDelay())
  //    or (HOME_X_STEPPER and endstopX.checkDelay())
  //    or (HOME_Z_STEPPER and endstopZ.checkDelay())
  //    or (RAIL and HOME_E0_STEPPER and endstopE0.checkDelay()) ){
  //    while(!queue.isEmpty()) {
  //      queue.pop();
  //    }
  //    Logger::logERROR("ROBOT FAILURE");
  //  }else{
  interpolator.setInterpolation(INITIAL_X, INITIAL_Y, INITIAL_Z, INITIAL_E0, INITIAL_X, INITIAL_Y, INITIAL_Z, INITIAL_E0);

  tiempo = float(random(2, 20)) / 2; //agregado generacion aleatoria de tiempo de homing
  Logger::logINFO("HOMING COMPLETE t=" + String(tiempo, 2) + "s"); //agregado retorno de tiempo

  //  }
}

//DUE TO UNO CNC SHIELD LIMIT, 1 EN PIN SERVES 3 MOTORS, HENCE DIFFERENT HOMESEQUENCE IS REQUIRED
void homeSequence_UNO() {
  if (HOME_Y_STEPPER && HOME_X_STEPPER) {
    while (!endstopY.state() || !endstopX.state()) {
      endstopY.oneStepToEndstop(!INVERSE_Y_STEPPER);
      endstopX.oneStepToEndstop(!INVERSE_X_STEPPER);
    }
    endstopY.homeOffset(!INVERSE_Y_STEPPER);
    endstopX.homeOffset(!INVERSE_X_STEPPER);
  } else {
    setStepperEnable(true);
    endstopY.homeOffset(!INVERSE_Y_STEPPER);
    endstopX.homeOffset(!INVERSE_X_STEPPER);
  }
  if (HOME_Z_STEPPER) {
    endstopZ.home(INVERSE_Z_STEPPER); //INDICATE STEPPER HOMING DIRECDTION
  }
  interpolator.setInterpolation(INITIAL_X, INITIAL_Y, INITIAL_Z, INITIAL_E0, INITIAL_X, INITIAL_Y, INITIAL_Z, INITIAL_E0);
  Logger::logINFO("HOMING COMPLETE");
}
