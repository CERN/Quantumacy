
Quantum-Key-Distribution
========================

A modified BB84 protocol utilizing emulated photons for Quantum Key Distribution (QKD).

Point
-----

Considering that we don't have an access to Quantum Computer yet, we will utilize emulated photons for key distribution. A protocol is modified - the common attacking methods such as eavesdropping can be avoided by the channel (classical server in this case) controlling pulses. Emulated photons in this case are in ideal environment, thus we use perfect single photon source. 

Example
-------

Quantum channel is initiated. Both **Bob** (receiver) and **Alice** (sender) known the ip address of this quantum channel.

**input:**

.. code-block:: python

   from channel import public_channel
   public_channel.initiate_server()

**server output:**

.. code-block::

   initiated the channel on xxx.xxx.x.xxx:xxxx, waiting for clients...

Bob starts listening to quantum channel.

**input:**

.. code-block:: python

   from receiver import receiver
   bob = receiver()
   bob.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   bob.listen_quantum()

**server output:**

.. code-block::

   xxx.xxx.x.xxx:xxxx has connected.

Alice sends a photon pulse to Bob.

**input:**

.. code-block:: python

   from sender import sender
   alice = sender()
   alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   photon_pulse = alice.create_photon_pulse()
   alice.send_photon_pulse(photon_pulse)

**server output:**

.. code-block::

   xxx.xxx.x.xxx:xxxx has connected.
   xxx.xxx.x.xxx:xxxx: qpulse:170
   xxx.xxx.x.xxx:xxxx: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alice and Bob reset their sockets.

**input:**

.. code-block:: python

   bob.reset_socket()

**input 2:**

.. code-block:: python

   alice.reset_socket()

After quantum channel is closed, classical channel is initiated. Both Bob and Alice known the ip address of this classical channel.

**input:**

.. code-block:: python

   from channel import public_channel
   public_channel.initiate_server()

Bob listens to public classical channel.

**input:**

.. code-block:: python

   bob.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   bob.listen_classical()

Alice sends her basis to Bob over public classical channel.

**input:**

.. code-block:: python

   alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   alice.send_classical_bits(alice.bases)

Alice listens to public classical channel.

**input:**

.. code-block:: python

   alice.reset_socket()
   alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   alice.listen_classical()

Bob sends his randomly measured basis over public classical channel.

.. code-block:: python

   bob.reset_socket()
   bob.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   bob.send_classical_bits(bob.bases)

Alice & Bob validate their shared bases, whether or not they are similar enough, then they can notify each other.

**input 1:**

.. code-block:: python

   decision = alice.validate()

**input 2:**

.. code-block:: python

   decision = bob.validate()

Finally, Alice & Bob exchange their decisions on classical public channel.

Bob listens to public classical channel.

**input:**

.. code-block:: python

   bob.reset_socket()
   bob.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   bob.listen_classical()

Alice sends her decision to Bob over public classical channel.

**input:**

.. code-block:: python

   alice.reset_socket()
   alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   alice.send_classical_bits(decision)

Alice listens to public classical channel.

**input:**

.. code-block:: python

   alice.reset_socket()
   alice.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   alice.listen_classical()

Bob sends his decision over public classical channel.

.. code-block:: python

   bob.reset_socket()
   bob.connect_to_channel('xxx.xxx.x.xxx', xxxx)
   bob.send_classical_bits()

If both of the users decide to use the key, Alice and Bob will have identical keys and then they can use some symmetric algorithm such as OTP (One Time Pad) or AES (Advanced Encryption Sequence) to communicate. Otherwise, this process is repeated.
