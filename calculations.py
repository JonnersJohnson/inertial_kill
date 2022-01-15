from graphics import *
import numpy as np
from data import *


# Calculates the minimum change of velocity (and hence speed) required to achieve intercept with target.
def min_intercept(p, tar):
    p_vel = np.array([p.velx, p.vely])
    t_vel = np.array([tar.velx, tar.vely])
    dv = np.subtract(p_vel, t_vel)
    p_x = np.array([p.x, p.y])
    t_x = np.array([tar.x, tar.y])
    dx = np.subtract(t_x, p_x)
    dx_norm = np.divide(dx, np.linalg.norm(dx))
    perp = np.array([-dx_norm[1], dx_norm[0]])
    if np.dot(perp, dv) < 0:
        perp = np.negative(perp)
    v_ch = np.multiply(np.negative(perp), np.dot(perp, dv))
    if np.dot(dx, dv) < 0:
        v_ch = np.subtract(v_ch, np.multiply(np.dot(dx_norm, dv), dx_norm))
    u = np.linalg.norm(v_ch)
    # z = np.abs(np.dot(dx, dv)) / np.dot(dx, dx)
    # v_ch = np.add(np.multiply(z, dx), dv)
    return [v_ch[0], v_ch[1], u]


# Generates missile at mothership and sends with initial boost velocity.
def launch(n, u, p):
    num = int(n)
    u = float(u)
    global particles
    if p.get() == "USA":
        mother = ship1
        target = ship2
    elif p.get() == "USSR":
        mother = ship2
        target = ship1
    if 0 < num <= mother.missiles and 10 + mother.boost_v > u >= min_intercept(mother, target)[2]:
        missile = Particle("missile", "yeoman", p.get(), mother.x, mother.y, mother.velx, mother.vely)
        p_x = np.array([mother.x, mother.y])
        t_x = np.array([target.x, target.y])
        u_min = np.array(min_intercept(missile, target)[0:2])
        dx = np.subtract(t_x, p_x)
        dx_norm = np.divide(dx, np.linalg.norm(dx))
        u_rel = u**2 - np.dot(u_min, u_min)
        du = np.add(np.multiply(u_rel, dx_norm), u_min)
        missile.velx += du[0]
        missile.vely += du[1]
        if u > mother.boost_v:
            missile.dv -= u - mother.boost_v
        missile.target = target
        missile.tvelx0 = target.velx
        missile.tvely0 = target.vely
        missile.missiles = num
        dv = np.array([missile.target.velx - missile.velx, missile.target.vely - missile.vely])
        v = (np.linalg.norm(dv))**0.5
        if v != 0:
            missile.m_req = target.defence / (v + missile.dv)
        else:
            missile.m_req = "na"
        mother.missiles -= num
        particles.append(missile)
        draw(particles, canvas)


# Changes course of in-flight missile to reacquire intercept with target (minimum velocity change).
def course_correct(missile):
    dv = np.array([missile.target.velx - missile.tvelx0, missile.target.vely - missile.tvely0])
    missile.tvelx0 = missile.target.velx
    missile.tvely0 = missile.target.vely
    u = np.linalg.norm(dv)
    if u < missile.dv:
        if dv[0] + dv[1] != 0:
            a = min_intercept(missile, missile.target)
            missile.velx += a[0]
            missile.vely += a[1]
            missile.dv -= a[2]
            # missile.velx += dv[0]
            # missile.vely += dv[1]
            # missile.dv -= u
        dv = np.array([missile.target.velx - missile.velx, missile.target.vely - missile.vely])
        v = (np.linalg.norm(dv))**0.5
        if v != 0:
            missile.m_req = missile.target.defence / (v + missile.dv)
        else:
            missile.m_req = "na"
    elif u >= missile.dv:
        missile.velx += (missile.dv / u) * dv[0]
        missile.vely += (missile.dv / u) * dv[1]
        missile.dv = 0
        missile.faction = "dead"


# Checks if missile will reach target during step. If so, calculates outcome of the interaction.
def check_int(missile, dt):
    global particles
    t = missile.target
    dv = np.array([t.velx - missile.velx, t.vely - missile.vely])
    v = np.linalg.norm(dv)
    dx = np.array([t.x - missile.x, t.y - missile.y])
    x = np.linalg.norm(dx)
    if missile.faction != "dead" and x <= v * float(dt):
        missile.missiles = np.floor(missile.missiles * (4 - t.mdef)/4)
        if missile.missiles >= missile.m_req:
            missile.target.faction = "dead"
        particles.remove(missile)
        if t.missiles >= t.mdef:
            t.missiles -= t.mdef
        else:
            t.missiles = 0


# Changes course of ship by specified speed and bearing.
def change_course(dv, bearing, p):
    deltav = float(dv)
    global particles, command_mdv
    if p.get() == "USA":
        particle = ship1
        target = ship2
    elif p.get() == "USSR":
        particle = ship2
        target = ship1
    if deltav <= particle.dv:
        theta = np.deg2rad(float(bearing))
        particle.velx += deltav * np.sin(theta)
        particle.vely += deltav * np.cos(theta)
        particle.dv -= deltav
        draw(particles, canvas)
    if particle.p_type == "ship":
        particle.req_dv = min_intercept(particle, target)[2]


# Calculates required delta v to intercept target.
def req_dv(p):
    if p.get() == "USA":
        particle = ship1
        target = ship2
    elif p.get() == "USSR":
        particle = ship2
        target = ship1
    return min_intercept(particle, target)[2]


# Moves time forward by specified amount.
def step_forward(particles, dt, canvas):
    for particle in particles:
        if particle.p_type == "missile" and particle.faction != "dead":
            course_correct(particle)
            check_int(particle, dt)
        particle.x += particle.velx * float(dt)
        particle.y += particle.vely * float(dt)
    draw(particles, canvas)


# Selects ship based on active faction.
def part_select(p):
    if p.get() == "USA":
        particle = ship1
    elif p.get() == "USSR":
        particle = ship2
    return particle


# Commits specified missiles to defence of the ship.
def defcommit(n, p):
    ship = part_select(p)
    if n >= 0 and n <= ship.missiles:
        if n < 4:
            ship.mdef = n
        else:
            ship.mdef = 4
        draw(particles, canvas)

