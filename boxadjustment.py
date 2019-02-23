## UD - updown
## LR - leftright

UD_error_prior = 0
UD_integral = 0
UD_KP = 1
UD_KI = 0
UD_KD = 0

LR_error_prior = 0
LR_integral = 0
LR_KP = 1
LR_KI = 0
LR_KD = 0

goal = 0

def getDistance(p1, p2):
   dx = p1[0] - p2[0]
   dy = p1[1] - p2[1]
   return sqrt(dx*dx + dy*dy) ###sqrt?

while True:
   ### given 4 points
   point1 = [x1, y1]
   point2 = [x2, y2]
   point3 = [x3, y3]
   point4 = [x4, y4]

   topDistance = getDistance(point1, point2)
   rightDistance = getDistance(point2, point3)
   bottomDistance = getDistance(point3, point4)
   leftDistance = getDistance(point4, point1)

   UD_error = topDistance - bottomDistance
   UD_integral = UD_integral + (UD_error * iteration_time)
   UD_derivative = (UD_error – UD_error_prior)/iteration_time
   UD_output = KP*UD_error + KI*UD_integral + KD*UD_derivative ### bias?
   UD_error_prior = UD_error

   LR_error = topDistance - bottomDistance
   LR_integral = LR_integral + (LR_error * iteration_time)
   LR_derivative = (LR_error – LR_error_prior)/iteration_time
   LR_output = KP*LR_error + KI*LR_integral + KD*LR_derivative ### bias?
   LR_error_prior = LR_error