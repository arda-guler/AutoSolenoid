import femm
import os
import matplotlib.pyplot as plt

class Coil:
    def __init__(self, N, L, I, r_in, D_wire):

        if D_wire * N < L:
            print("Coil not tightly wound.")

        self.N = N # number of turns
        self.L = L # mm, length
        self.I = I # A, current
        self.r_in = r_in # mm, inner radius
        self.D_wire = D_wire # mm, wire diameter

        if D_wire % 1 == 0:
            self.mtlstr = str(int(D_wire)) + "mm"
        else:
            self.mtlstr = str(D_wire) + "mm"

        self.r_out = self.r_in + (int(self.N / int(self.L / self.D_wire)) + 1) * self.D_wire # mm, outer radius
        self.N_radial = int(self.N / int(self.L / self.D_wire)) + 1 # number of radial layers of winding
        self.r_avg = (self.r_in + self.r_out) * 0.5

    def get_rect(self):
        x1, y1 = self.r_in, self.L / 2
        x2, y2 = self.r_out, -self.L / 2

        return x1, y1, x2, y2

class Plunger:
    def __init__(self, r, L, r_s, L_s, mtl):
        self.r = r
        self.L = L
        self.r_s = r_s
        self.L_s = L_s
        self.mtl = mtl

    def get_nodes(self):
        n0 = [0, self.L * 0.5 - self.L_s]
        n1 = [self.r_s, self.L * 0.5 - self.L_s]
        n2 = [self.r_s, self.L * 0.5]
        n3 = [self.r, self.L * 0.5]
        n4 = [self.r, -self.L * 0.5]
        n5 = [0, -self.L * 0.5]

        nodes = [n0, n1, n2, n3, n4, n5]
        labelpos = [(n2[0] + n4[0]) * 0.5, (n2[1] + n4[1]) * 0.5]
        return nodes, labelpos

    def get_rect(self):
        x1, y1 = 0, self.L / 2
        x2, y2 = self.r, -self.L / 2

        return x1, y1, x2, y2

class MagneticCore:
    def __init__(self, coil, r_minor, L_in, t_r, t_a1, t_a2, mtl):
        self.coil = coil
        self.r_minor = r_minor
        self.L_in = L_in
        self.t_r = t_r
        self.t_a1 = t_a1
        self.t_a2 = t_a2
        self.mtl = mtl

    def get_nodes(self):
        x1, y1, x2, y2 = self.coil.get_rect()
        n0 = [0, y1 + self.t_a1]
        n1 = [x2 + self.t_r, y1 + self.t_a1]
        n2 = [x2 + self.t_r, y2 - self.t_a2]
        n3 = [x1, y2 - self.t_a2]
        n4 = [x1, y2]
        n5 = [x2, y2]
        n6 = [x2, y1]
        n7 = [x1, y1]
        n8 = [x1, y1 - self.L_in]
        n9 = [0, y1 - self.L_in]
        nodes = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]

        xlabel, ylabel = (n0[0] + n7[0]) * 0.5, (n0[1] + n7[1]) * 0.5
        return nodes, [xlabel, ylabel]

def FEMM_rectnodes(x1, y1, x2, y2):
    femm.mi_addnode(x1, y1)
    femm.mi_addnode(x2, y1)
    femm.mi_addnode(x2, y2)
    femm.mi_addnode(x1, y2)

def FEMM_rectlines(x1, y1, x2, y2):
    femm.mi_addsegment(x1, y1, x2, y1)
    femm.mi_addsegment(x2, y1, x2, y2)
    femm.mi_addsegment(x2, y2, x1, y2)
    femm.mi_addsegment(x1, y2, x1, y1)

def FEMM_rect(x1, y1, x2, y2):
    FEMM_rectnodes(x1, y1, x2, y2)
    FEMM_rectlines(x1, y1, x2, y2)

def FEMM_coillabel(coil):
    x1, y1, x2, y2 = coil.get_rect()
    x, y = (x1 + x2) * 0.5, (y1 + y2) * 0.5

    femm.mi_addblocklabel(x, y)
    femm.mi_selectlabel(x, y)
    femm.mi_setblockprop(coil.mtlstr, 1, 1e-3, "circuit_solenoid", 0, 0, coil.N)
    femm.mi_clearselected()

    xout, yout = x2 * 3, 0
    femm.mi_addblocklabel(xout, yout)
    femm.mi_selectlabel(xout, yout)
    femm.mi_setblockprop("Air", 1, 1e-3, "<None>", 0, 0, 1)
    femm.mi_clearselected()

def FEMM_plungerlabel(plunger, offset):
    x1, y1, x2, y2 = plunger.get_rect()
    y1 += offset
    y2 += offset
    x, y = (x1 + x2) * 0.5, (y1 + y2) * 0.5

    femm.mi_addblocklabel(x, y)
    femm.mi_selectlabel(x, y)
    femm.mi_setblockprop(plunger.mtl, 1, 1e-3, "<None>", 0, 0, 0)
    femm.mi_clearselected()

def FEMM_circuit(I):
    femm.mi_addcircprop("circuit_solenoid", I, 1)

def FEMM_GenerateCore(magcore):
    nodes, labelpos = magcore.get_nodes()
    for n in nodes:
        femm.mi_addnode(n[0], n[1])

    connectlist = []
    for idx_n in range(len(nodes)):
        connectlist.append([nodes[idx_n - 1], nodes[idx_n]])

    for cn in connectlist:
        femm.mi_addsegment(cn[0][0], cn[0][1], cn[1][0], cn[1][1])

    femm.mi_addblocklabel(labelpos[0], labelpos[1])

    femm.mi_selectlabel(labelpos[0], labelpos[1])
    femm.mi_setblockprop(magcore.mtl, 1, 1e-3, "<None>", 0, 0, 0)
    femm.mi_clearselected()

def FEMM_GetMaterials(coil, plunger, core):
    mtls = [coil.mtlstr, plunger.mtl, core.mtl]

    # don't get duplicates
    mtls_sanitized = []
    [mtls_sanitized.append(x) for x in mtls if x not in mtls_sanitized]
    mtls_sanitized.append("Air")

    for mtl in mtls_sanitized:
        femm.mi_getmaterial(mtl)

def FEMM_forceintegral(x, y):
    femm.mo_selectblock(x, y)
    z_force = femm.mo_blockintegral(19) # in z direction (r should be 0)
    femm.mo_clearblock()
    return z_force

def FEMM_GenerateCoil(coil):
    x1, y1, x2, y2 = coil.get_rect()
    FEMM_rect(x1, y1, x2, y2)
    FEMM_circuit(coil.I)
    FEMM_coillabel(coil)

def FEMM_GeneratePlunger(plunger, plunger_offset):
    nodes, labelpos = plunger.get_nodes()

    for n in nodes:
        n[1] = n[1] + plunger_offset

    for n in nodes:
        femm.mi_addnode(n[0], n[1])

    connectlist = []
    for idx_n in range(len(nodes)):
        connectlist.append([nodes[idx_n - 1], nodes[idx_n]])

    for cn in connectlist:
        femm.mi_addsegment(cn[0][0], cn[0][1], cn[1][0], cn[1][1])

    femm.mi_addblocklabel(labelpos[0], labelpos[1])

    femm.mi_selectlabel(labelpos[0], labelpos[1])
    femm.mi_setblockprop(plunger.mtl, 1, 1e-3, "<None>", 0, 0, 0)
    femm.mi_clearselected()

    return labelpos[0], labelpos[1]

def generate_FEMM_design(coil, plunger, magcore, plunger_offset=0, plunger_max_offset=0, filename="autocoil", dirname="autocoil", view_padding=10):
    femm.openfemm(femmpath="C:/femm42/bin")

    # axissymmetric magnetics problem in millimeters
    femm.newdocument(0)
    femm.mi_probdef(0, "millimeters", "axi", 1E-8, 0, 30)

    bitmap_filename = dirname + "/" + filename + ".bmp"
    femm_filename = dirname + "/" + filename + ".fem"

    # get materials
    FEMM_GetMaterials(coil, plunger, magcore)

    # create components
    FEMM_GenerateCoil(coil)
    x_plunger, y_plunger = FEMM_GeneratePlunger(plunger, plunger_offset)
    FEMM_GenerateCore(magcore)

    # create boundary
    femm.mi_makeABC()

    # save and analyze
    femm.mi_saveas(femm_filename)
    femm.mi_createmesh()
    femm.mi_analyse(0)

    # post-process
    femm.mi_loadsolution()
    z_force = FEMM_forceintegral(x_plunger, y_plunger)
    femm.mo_hidegrid()
    femm.mo_showdensityplot(1, 0, 1, 0, "bmag")

    x1_zoom = -view_padding
    y1_zoom = coil.L * 0.5 + magcore.t_a1 + view_padding
    x2_zoom = coil.r_out + magcore.t_r + view_padding
    y2_zoom = plunger_max_offset - plunger.L * 0.5 - view_padding
    femm.mo_zoom(x1_zoom, y2_zoom, x2_zoom, y1_zoom)
    femm.mo_savebitmap(bitmap_filename)

    # we are done
    femm.closefemm()

    return z_force, bitmap_filename

def save_movie(files):
    import moviepy.video.io.ImageSequenceClip as mov
    files_mirror = files[0:-1]
    files_mirror.reverse()
    files = files + files_mirror
    clip = mov.ImageSequenceClip(files, fps=4)
    clip.write_videofile(files[0][:-7] + ".mp4")

def makedir(dirname):
    if not os.path.exists(dirname + "/"):
        os.makedirs(dirname)

def autoAnalyze(inputs):
    N_coil = inputs[0]
    L_coil = inputs[1]
    I_coil = inputs[2]
    r_in_coil = inputs[3]
    D_wire = inputs[4]
    r_plunger = inputs[5]
    L_plunger = inputs[6]
    r_spring = inputs[7]
    L_spring = inputs[8]
    mtl_plunger = inputs[9]
    L_stroke = inputs[10]
    r_minor_core = inputs[11]
    L_in_core = inputs[12]
    t_r_core = inputs[13]
    t_a1_core = inputs[14]
    t_a2_core = inputs[15]
    mtl_core = inputs[16]
    d_stroke = inputs[17]
    view_padding = inputs[18]
    filename_main = inputs[19]
    export_video = inputs[20]

    print("Generating design...")
    s1 = Coil(N_coil, L_coil, I_coil, r_in_coil, D_wire)
    p1 = Plunger(r_plunger, L_plunger, r_spring, L_spring, mtl_plunger)
    c1 = MagneticCore(s1, r_minor_core, L_in_core, t_r_core, t_a1_core, t_a2_core, mtl_core)

    y1 = L_coil * 0.5
    if y1 - L_in_core < L_plunger * 0.5 + 1:
        plunger_offset = (L_plunger * 0.5 + 1) - (y1 - L_in_core)
    else:
        plunger_offset = 0

    plunger_offset *= -1
    n_stroke = int(L_stroke / d_stroke) + 1

    makedir(filename_main)

    print("Starting analysis...")
    forces = []
    offsets = []
    bitmap_filenames = []
    for i in range(n_stroke):
        print("Analysis " + str(i + 1) + " of " + str(n_stroke) + " in progress...")
        current_offset = plunger_offset - i * d_stroke

        if i < 10:
            filename = filename_main + "00" + str(i)
        elif i < 100:
            filename = filename_main + "0" + str(i)
        else:
            filename = filename_main + str(i)

        current_force, bitmap_filename = generate_FEMM_design(s1, p1, c1, current_offset,
                                                              plunger_offset - n_stroke * d_stroke,
                                                              filename, filename_main, view_padding)
        offsets.append(i * d_stroke)
        forces.append(current_force)
        bitmap_filenames.append(bitmap_filename)

    if export_video:
        print("Generating movie...")
        save_movie(bitmap_filenames)

    print("Generating force plot...")
    plt.plot(offsets, forces)
    plt.xlabel("Plunger stroke position (mm)")
    plt.ylabel("Plunger force (N)")
    plt.title("Force vs. Plunger Position")
    plt.grid()
    print("Saving force plot...")
    plt.savefig(filename_main + "/" + filename_main + "_force.png")
    print("Displaying force plot...")
    plt.show()

    print("Done.")
