import numpy as np

class hst_data:

    def __init__(self, fn, ncells=[None, None, None], MHD_flag=False, cool_flag=False):

        """Read hst and return structured numpy dict.
        Keyword Arguments:
        fn -- 
        """

        hdr = []
        with open(fn, 'r') as fp:
            while True:
                l = fp.readline()
                if l[0] != '#':
                    raise Exception("No header in %s found!" %(fn))
                if '[1]' in l:
                    hdr = [i.split("=")[1].strip() for i in l[1:].split("[") if ']' in i]
                    break

        r = np.loadtxt(fn, dtype={'names' : hdr, 'formats' : len(hdr) * (float,)})

        if None in ncells:
            raise ValueError('Invalid argument for ncells ...')
        else:
            cells =  np.product(np.array(ncells))


        self.dict = r

        self.time  = self.dict['time']
        self.dt    = self.dict['dt']

        self.mass_tot  = self.dict['mass']

        self.mom1  = self.dict['1-mom']
        self.mom2  = self.dict['2-mom']
        self.mom3  = self.dict['3-mom']

        self.KE1   = self.dict['1-KE']
        self.KE2   = self.dict['2-KE']
        self.KE3   = self.dict['3-KE']
        self.E_tot = self.dict['tot-E']

        if cool_flag:
            self.cold_gas          = self.dict['cold_gas']
            self.tcool_avg         = self.dict['tcool_sum']/cells
            self.cold_gas_fraction = self.cold_gas/self.mass_tot

        self.rho_avg    = self.dict['rho_sum']   /cells
        self.rho_sq_avg = self.dict['rho_sq_sum']/cells

        self.cs_avg     = self.dict['c_s_sum']/cells

        if MHD_flag:

            self.Pth_avg = self.dict['Pth_sum']/cells
            self.PB_avg  = self.dict['PB_sum'] /cells
            self.Bx_avg  = self.dict['Bx_sum'] /cells
            self.By_avg  = self.dict['By_sum'] /cells
            self.Bz_avg  = self.dict['Bz_sum'] /cells

            self.B_abs_avg = np.sqrt(self.PB_avg*2)

            self.dB = np.roll(self.B_abs_avg,-1) - self.B_abs_avg
            self.dt = self.time[1] - self.time[0]


        self.KE_tot   = self.KE1+self.KE2+self.KE3
        self.turb_vel = np.sqrt(self.KE_tot*2/self.mass_tot)

        self.clumping_factor = self.rho_sq_avg/self.rho_avg**2

        

        
        