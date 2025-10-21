
class usb_mf_motordriver:
    def __init__(self ):
        self.m01_stdy       = 0
        self.m23_stdy       = 0
                
        self.m0_in1         = 0
        self.m0_in2         = 0
        self.m0_pwm         = 0
        
        self.m1_in1         = 0
        self.m1_in2         = 0
        self.m1_pwm         = 0
        
        self.m2_in1         = 0
        self.m2_in2         = 0
        self.m2_pwm         = 0
        
        self.m3_in1         = 0
        self.m3_in2         = 0
        self.m3_pwm         = 0        
        
        self.all_motors     = 0
        self.which_motor    = 0
        
    def change_stby ( self ):    
        if ( self.m01_stdy==0 ):
            self.m01_stdy = 1;
        else:
            self.m01_stdy = 0;

        if ( self.m23_stdy==0 ):
            self.m23_stdy = 1;
        else:
            self.m23_stdy = 0;
        
        
    def increase_speed( self ):
        print("Increase : ",end="")
        
        if ( self.all_motors==1 or self.which_motor==0 ):
            self.m0_pwm = self.m0_pwm + 10
            self.m0_pwm = min ( 255, self.m0_pwm)
        if ( self.all_motors==1 or self.which_motor==1 ):
            self.m1_pwm = self.m1_pwm + 10
            self.m1_pwm = min ( 255, self.m1_pwm)
        if ( self.all_motors==1 or self.which_motor==2 ):
            self.m2_pwm = self.m2_pwm + 10
            self.m2_pwm = min ( 255, self.m2_pwm)
        if ( self.all_motors==1 or self.which_motor==3 ):
            self.m3_pwm = self.m3_pwm + 10     
            self.m3_pwm = min ( 255, self.m3_pwm)
        
    
    def decrease_speed( self ):    
        print("Decrease : ",end="")
        
        if ( self.all_motors==1 or self.which_motor==0 ):
            self.m0_pwm = self.m0_pwm - 10
            self.m0_pwm = max ( 0, self.m0_pwm)
        if ( self.all_motors==1 or self.which_motor==1 ):
            self.m1_pwm = self.m1_pwm - 10
            self.m1_pwm = max ( 0, self.m1_pwm)
        if ( self.all_motors==1 or self.which_motor==2 ):
            self.m2_pwm = self.m2_pwm - 10
            self.m2_pwm = max ( 0, self.m2_pwm)
        if ( self.all_motors==1 or self.which_motor==3 ):
            self.m3_pwm = self.m3_pwm - 10     
            self.m3_pwm = max ( 0, self.m3_pwm)            
        
        
    def set_direction ( self, new_dir ):        
        print("Direction : ",end="")
        if ( new_dir=="CW" ):
            new_in1 = 1
            new_in2 = 0
        elif ( new_dir=="CCW" ):
            new_in1 = 0
            new_in2 = 1
        elif ( new_dir=="Brake" ):
            new_in1 = 1
            new_in2 = 1            
        else:                       #STOP
            new_in1 = 0
            new_in2 = 0

        
        if ( self.all_motors==1 or self.which_motor==0 ):
            self.m0_in1 = new_in1
            self.m0_in2 = new_in2
        if ( self.all_motors==1 or self.which_motor==1 ):
            self.m1_in1 = new_in1
            self.m1_in2 = new_in2      
        if ( self.all_motors==1 or self.which_motor==2 ):
            self.m2_in1 = new_in1
            self.m2_in2 = new_in2
        if ( self.all_motors==1 or self.which_motor==3 ):
            self.m3_in1 = new_in1
            self.m3_in2 = new_in2            
        
    def get_cdcdata( self ):
        cdcdata = [0, 0, self.m0_pwm, 0, self.m1_pwm, 0, self.m2_pwm, 0, self.m3_pwm]
        
        if ( self.m01_stdy==1 ):
            cdcdata[0] = cdcdata[0] + 1;
        if ( self.m23_stdy==1 ):
            cdcdata[0] = cdcdata[0] + 2;    
    
        if ( self.m0_in1==1 ):
            cdcdata[1] = cdcdata[1] + 1;
        if ( self.m0_in2==1 ):
            cdcdata[1] = cdcdata[1] + 2;      
    
        if ( self.m1_in1==1 ):
            cdcdata[3] = cdcdata[3] + 1;
        if ( self.m1_in2==1 ):
            cdcdata[3] = cdcdata[3] + 2;     

        if ( self.m2_in1==1 ):
            cdcdata[5] = cdcdata[5] + 1;
        if ( self.m2_in2==1 ):
            cdcdata[5] = cdcdata[5] + 2;     

        if ( self.m3_in1==1 ):
            cdcdata[7] = cdcdata[7] + 1;
        if ( self.m3_in2==1 ):
            cdcdata[7] = cdcdata[7] + 2;      
    
        return cdcdata
        
    def current_state( self ):        
        print("")
        print("All Motors : ",end="")
        print(self.all_motors)
                
        print("Which Motor : ",end="")
        print(self.which_motor)
        
        print("M01_STDY : ",end="")
        print(self.m01_stdy)        
        print("M23_STDY : ",end="")
        print(self.m23_stdy)            
    
        print("")    
        print("M0_IN1 : ",end="")
        print(self.m0_in1)        
        print("M0_IN2 : ",end="")
        print(self.m0_in2)          
        print("M0_PWM : ",end="")
        print(self.m0_pwm)        
        
        print("M1_IN1 : ",end="")
        print(self.m1_in1)        
        print("M1_IN2 : ",end="")
        print(self.m1_in2)          
        print("M1_PWM : ",end="")
        print(self.m1_pwm)

        print("M2_IN1 : ",end="")
        print(self.m2_in1)        
        print("M2_IN2 : ",end="")
        print(self.m2_in2)          
        print("M2_PWM : ",end="")
        print(self.m2_pwm)

        print("M3_IN1 : ",end="")
        print(self.m3_in1)        
        print("M3_IN2 : ",end="")
        print(self.m3_in2)          
        print("M3_PWM : ",end="")
        print(self.m3_pwm)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        