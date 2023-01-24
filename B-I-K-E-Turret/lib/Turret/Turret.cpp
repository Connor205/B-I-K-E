#include "Turret.hpp"
#include <Constants.hpp>

Turret::Turret() {
	turretMotor = StepperMotor(TURRET_STEP_PIN, TURRET_DIR_PIN, TURRET_OUTPUT_GEAR_RATIO);
}

Turret::init() {
	turretMotor.init();
}

Turret::calibrate() {
	turretMotor.calibrate();
}