import numpy as np
import sys

class hst_data:

    def __init__(self, fn, ncells=[None, None, None], box_size=[None, None, None],\
                 MHD_flag=False, cool_flag=False, shift_flag=False, Chi=None, verbose=False):

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

        # try:
        #     r = np.loadtxt(fn, dtype={'names' : hdr, 'formats' : len(hdr) * (float,)})
        #     if verbose:
        #         print(f"history.py: hst_data :: History file loaded for {fn} ...")
        # except:
        #     print(f"history.py: hst_data :: File couldn't be loaded for {fn} ...")
        #     # return -1

        if None in ncells:
            raise ValueError('hst_data() :: Invalid argument for ncells ...')
        else:
            cells =  np.product(np.array(ncells))
            self.ncell_x = ncells[0]
            self.ncell_y = ncells[1]
            self.ncell_z = ncells[2]

        # print('boxsize: ', type(box_size))
        # print('ncells : ', type(ncells))

        if None in box_size:
            raise ValueError('hst_data() :: Invalid argument for box_size...')
        else:
            self.box_size_x = box_size[0]
            self.box_size_y = box_size[1]
            self.box_size_z = box_size[2]


        if Chi is None:
            print("Assuming a Chi of 100...")
            Chi = 100.0
        self.Chi = Chi

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
            self.cold_gas            = self.dict['cold_gas']
            # self.tcool_avg         = self.dict['tcool_sum']/cells
            self.cold_gas_fraction   = self.cold_gas/self.mass_tot

            #* Front position for a box size of 1.0
            self.front_posn_fraction = self.cold_gas_fraction
            self.front_posn_fraction /= self.Chi * (1-self.cold_gas_fraction) + self.cold_gas_fraction

            self.total_cooling = self.dict['total_cooling']

            #* Luminosity calculation
            dcool = np.roll(self.total_cooling, -1) - self.total_cooling 
            dt    = np.roll(self.time, -1) - self.time

            dz = self.box_size_z / self.ncell_z
            dy = self.box_size_y / self.ncell_y
            dx = self.box_size_x / self.ncell_x

            self.luminosity  = (dcool/dt)[1:-1] * dx * dy * dz
            self.luminosity /= (self.box_size_x * self.box_size_y)



        self.rho_avg    = self.dict['rho_sum']   /cells
        self.rho_sq_avg = self.dict['rho_sq_sum']/cells

        self.cs_avg        = self.dict['c_s_sum']/cells

        if MHD_flag:

            self.Pth_avg = self.dict['Pth_sum']/cells
            self.PB_avg  = self.dict['PB_sum'] /cells
            self.Bx_avg  = self.dict['Bx_sum'] /cells
            self.By_avg  = self.dict['By_sum'] /cells
            self.Bz_avg  = self.dict['Bz_sum'] /cells

            self.B_abs_avg = np.sqrt(self.PB_avg*2)

            self.dB = np.roll(self.B_abs_avg,-1) - self.B_abs_avg
            self.dt = self.time[1] - self.time[0]

        if shift_flag:
            self.shift_velocity = self.dict['front_velocity']


        self.KE_tot   = self.KE1+self.KE2+self.KE3
        self.turb_vel = np.sqrt(self.KE_tot*2/self.mass_tot)

        self.clumping_factor = self.rho_sq_avg/self.rho_avg**2



    def overflow_cut(self, hst_var, cut_var=None, cut_list=[0.1, 0.9]):
    
        # N_last = 2000
        aft_cut = np.copy(hst_var)
        time = np.copy(self.time)

        if cut_var is None:
            cut_var = self.cold_gas_fraction
        cold_fraction = np.copy(cut_var)

        if len(aft_cut) != len(time):
            # This means hst_var is a derivative
            dN = len(time) - len(aft_cut)
            time          = time         [int(dN/2):-int(dN/2)]
            cold_fraction = cold_fraction[int(dN/2):-int(dN/2)]

        box_full_hot  = np.argwhere(cold_fraction<cut_list[0])

        if len(box_full_hot)!=0:
            aft_cut       = aft_cut       [:np.min(box_full_hot)]
            time          = time          [:np.min(box_full_hot)]
            cold_fraction = cold_fraction [:np.min(box_full_hot)]

        box_full_cold = np.argwhere(cold_fraction>cut_list[1])

        if len(box_full_cold)!=0:
            aft_cut = aft_cut [:np.min(box_full_cold)]
            time    = time    [:np.min(box_full_cold)]


        return time, aft_cut