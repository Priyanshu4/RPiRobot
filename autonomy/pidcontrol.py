class PIDController(object):
    
    def __init__(self, kP = 0, kI = 0, kD = 0, deadband = 0):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.deadband = deadband
        self.reset()

    def resetIntegrator(self):
        self.integrator = 0

    def reset(self):
        self.resetIntegrator()
        self.prevError = None

    def deadbandError(self, error):
          if error < self.deadband and error > self.deadband:
              error = 0
          elif error > self.deadband:
              error = error - self.deadband
          elif error < -self.deadband:
              error = error + self.deadband
          return error
  
    def executeControlLoop(self, error, deltaTime):
        error = self.deadbandError(error)
        self.integrator += error * deltaTime
        if self.prevError is None:
            derivative = 0
        else:
            derivative = (self.prevError - error) / deltaTime
        output = self.kP * error + self.kI * self.integrator + self.kD * derivative
        self.prevError = error
        return output