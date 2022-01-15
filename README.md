# inertial_kill
A 2D space battle simulator with realistic physics modelling.

This program models two ships engaged in long-range missile combat.
Each ship has a finite number of missiles, and both the missiles and ships have a finite ability to change their velocity (delta v).
Missiles will actively track their target, provided they have the delta v necessary to do so.
Missiles can only be lauched if their initial delta v is set high enough to achieve intercept. The "calculate" button displays this delta v.
Missile groups contain a certain number of missiles.

Combat is based on the ability for missiles to overcome a ship's point-defences. This ability is defined by the number of missiles in a group * their speed relative to the target.
If this value exceeds the value set for the ship (representing the strength of its defences and armour), the ship is destroyed.
