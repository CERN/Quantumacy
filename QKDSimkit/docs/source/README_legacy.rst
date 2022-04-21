
Quantum-Key-Distribution
========================

A modified BB84 protocol utilizing emulated photons for Quantum Key Distribution (QKD).

Point
-----

Considering that we don't have an access to Quantum Computer yet, we will utilize emulated photons for key distribution. A protocol is modified - the common attacking methods such as eavesdropping can be avoided by the channel (classical server in this case) controlling pulses. Emulated photons in this case are in ideal environment, thus we use perfect single photon source. 

Example
-------


* Quantum channel is initiated. Both **Bob** (receiver) and **Alice** (sender) known the ip address of the quantum channel.

.. code-block:: python

   from channel import public_channel
   public_channel.initiate_server()


* Bob starts listening to quantum channel.

.. code-block:: python

   from receiver import receiver
   bob = receiver()
   bob.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   bob.listen_quantum()


* Alice sends a photon pulse to Bob.

.. code-block:: python

   from sender import sender
   alice = sender()
   alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   photon_pulse = alice.create_photon_pulse()
   alice.send_photon_pulse(photon_pulse)


* Alice and Bob reset their sockets.

.. code-block:: python

   bob.reset_socket()

.. code-block:: python

   alice.reset_socket()


* 
  After the quantum channel is closed, a classical channel is initiated. Both Bob and Alice known the address of this classical channel.

* 
  Bob sends his basis to Alice over public classical channel and then listens for their shared basis.

.. code-block:: python

   bob.send('bob-other_bases', repr(bob.bases))
   bob.listen_for('alice', 'reconciled_key')


* Alice listens to Bob's bases, generates a key with its matching bases and sends it.

.. code-block:: python

   alice.listen_for('bob', 'other_bases')
   alice.generate_reconciled_key()
   alice.send('alice-reconciled_key', repr(alice.reconciled_key))


* Alice creates a key sends half of it to Bob, then waits for Bob's half

.. code-block:: python

   alice.create_keys()
   alice.send('alice-other_sub_key', repr(alice.sub_shared_key))
   alice.listen_for('bob', 'other_sub_key')


* Bob creates his key and listen Alice's half then he sends a half of his key.

.. code-block:: python

   bob.create_keys()
   bob.listen_for('alice', 'other_sub_key')
   bob.send('bob-other_sub_key', repr(bob.sub_shared_key))


* Alice & Bob validate their shared bases, then they notify each other.

.. code-block:: python

   alice.decision = alice.validate()
   alice.send('alice-other_decision', repr(alice.decision))
   alice.listen_for('bob', 'other_decision')

.. code-block:: python

   bob.decision = bob.validate()
   bob.listen_for('alice', 'other_decision')
   bob.send('bob-other_decision', repr(bob.decision))

If either Alice and Bob successfully validate the key, they have identical keys and they can use some symmetric algorithm such as OTP (One Time Pad) or AES (Advanced Encryption Sequence) to communicate. Otherwise, this process is repeated.
