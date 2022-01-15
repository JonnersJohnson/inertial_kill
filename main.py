from calculations import *
from data import *

# GUI layout definition
def calc_req_dv(p):
    command_mdv.delete(0, END)
    command_mdv.insert(0, round(req_dv(p), 2))


label_delta = Label(root, text="Delta V:", height=1, width=10)
label_delta.grid(row=0, column=1)
label_bear = Label(root, text="Bearing:", height=1, width=10)
label_bear.grid(row=1, column=1)
command_dv = Entry(root, width=10)
command_dv.grid(row=0, column=2)
command_bear = Entry(root, width=10)
command_bear.grid(row=1, column=2)
but_execute = Button(root, text="Execute", height=1, width=10, command=lambda:
                     change_course(command_dv.get(), command_bear.get(), p))
but_execute.grid(row=2, column=1)
but_calc = Button(root, text="Calculate", height=1, width=10, command=plot_course)
but_calc.grid(row=2, column=2)

label_interval = Label(root, text="Time step:", height=1, width=10)
label_interval.grid(row=3, column=1)
command_interval = Entry(root, width=10)
command_interval.grid(row=3, column=2)
command_interval.insert(0, "4.0")
but_step = Button(root, text="Step forward", height=1, width=20, command=lambda:
    step_forward(particles, command_interval.get(), canvas))
but_step.grid(row=4, column=1, columnspan=2)

p = StringVar()
p.set("USA")
label_faction = Label(root, text="Faction:")
label_faction.grid(row=5, column=1)
choose_fac = OptionMenu(root, p, "USA", "USSR")
choose_fac.grid(row=5, column=2)

label_missiles = Label(root, text="Missiles", height=1, width=20)
label_missiles.grid(row=6, column=1, columnspan=2)
label_mdv = Label(root, text="Delta V:", height=1, width=10)
label_mdv.grid(row=7, column=1)
command_mdv = Entry(root, width=10)
command_mdv.grid(row=7, column=2)
calc_req_dv(p)
label_mnum = Label(root, text="Number:", height=1, width=10)
label_mnum.grid(row=8, column=1)
command_mnum = Entry(root, width=10)
command_mnum.grid(row=8, column=2)
command_mnum.insert(0, "1")
but_launch = Button(root, text="Launch", height=1, width=10, command=lambda:
                     launch(command_mnum.get(), command_mdv.get(), p))
but_launch.grid(row=9, column=1)
but_mcalc = Button(root, text="Calculate", height=1, width=10, command=lambda: calc_req_dv(p))
but_mcalc.grid(row=9, column=2)

label_defence = Label(root, text="Defence", height=1, width=20)
label_defence.grid(row=10, column=1, columnspan=2)
label_mdef = Label(root, text="Number:", height=1, width=10)
label_mdef.grid(row=11, column=1)
command_mdef = Entry(root, width=10)
command_mdef.grid(row=11, column=2)
but_defcommit = Button(root, text="Commit", height=1, width=10, command=lambda:
                     defcommit(int(command_mdef.get()), p))
but_defcommit.grid(row=12, column=1)

# Begin game
draw(particles, canvas)
root.mainloop()