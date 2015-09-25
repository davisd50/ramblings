from collections import deque
from time import sleep

# We require some module-level variables to allow for message delivery

nodes = 4 # int total number of nodes (set this before instantiated any objects)
last_registered_node = None
#inbox ==> {target: {source: messages(deque): message(deque)}}
inbox = {target:{source:deque() for source in range(nodes)} for target in range(nodes)}

class messenger_offline(object):
    """Message library imulation for GCJ distributed
    
    Usage:
        Get our messenger and send some messages
        >>> from gcj.distributed.messenger import messenger_offline as messenger
        >>> myMessenger0 = messenger()
        >>> myMessenger0.MyNodeId()
        0
        
        >>> myMessenger1 = messenger()
        >>> myMessenger1.MyNodeId()
        1
        
        >>> myMessenger0.PutChar(1, 'a')
        >>> myMessenger0.PutChar(1, 'b')
        >>> myMessenger0.PutChar(1, 'c')
        >>> myMessenger0.PutInt(1, 1)
        >>> myMessenger0.PutInt(1, 2)
        >>> myMessenger0.PutInt(1, 3)
        >>> myMessenger0.Send(1)
        
        >>> source = myMessenger1.Receive(0)
        >>> source
        0
        
        >>> myMessenger1.GetChar(0)
        'a'
        >>> myMessenger1.GetChar(0)
        'b'
        >>> myMessenger1.GetChar(0)
        'c'
        >>> myMessenger1.GetInt(0)
        1
        >>> myMessenger1.GetInt(0)
        2
        >>> myMessenger1.GetInt(0)
        3
    """
    
    def __init__(self):
        global nodes, last_registered_node, inbox
        #import pdb;pdb.set_trace()
        if last_registered_node == None:
            last_registered_node = 0
        else:
            last_registered_node += 1
        if last_registered_node == nodes:
            raise IndexError("exceeded maximum number of available nodes")
        self.node = last_registered_node
        
        self._send_buffer = {node: deque() for node in range(nodes)}
        self._receive_buffer = {node: deque() for node in range(nodes)}
    
    @classmethod
    def NumberOfNodes(cls):
        return cls.nodes
    
    def MyNodeId(self):
        return self.node
    
    
    def PutChar(self, target, value):
        """Append a single character to the message. "value" should be a one-character
          string.
        """
        self._send_buffer[target].append(value)

    def PutInt(self, target, value):
        """Append a 32-bit integer to the message. The "value" will be truncated to
           the least meaningful 32 bits.
        """
        self._send_buffer[target].append(value)

    def PutLL(self, target, value):
        """Append a 64-bit integer to the message. The "value" will be truncated to
           the least meaningful 64 bits.
        """
        self._send_buffer[target].append(value)

    def Send(self, target):
        """Send the message that was accumulated in the appropriate buffer to the
        "target" instance, and clear the buffer for this instance.

        This method is non-blocking - that is, it does not wait for the receiver to
        call "Receive", it returns immediately after sending the message.
        """
        global inbox
        if target not in self._send_buffer or not self._send_buffer[target]:
            raise ValueError("expected queued message to send")
        inbox[self.MyNodeId()][target].append(self._send_buffer[target])
        self._send_buffer[target] = deque() #reset buffer
    
    def Receive(self, source):
        global inbox
        #import pdb;pdb.set_trace()
        while True:
            if source == -1:
                for source, messages in inbox[self.MyNodeId()]:
                    self._receive_buffer[source] = messages.popleft()
                    return source
            else:
                if inbox[source][self.MyNodeId()]:
                    self._receive_buffer[source] = inbox[source][self.MyNodeId()].popleft()
                    return source
            sleep(.0000001)

    def GetChar(self, source):
        """Retrieve a single-character string from the message."""
        return self._receive_buffer[source].popleft()

    def GetInt(self, source):
        """Retrieve a 32-bit integer from the message."""
        return self._receive_buffer[source].popleft()

    def GetLL(self, source):
        """Retrieve a 64-bit integer from the message."""
        return self._receive_buffer[source].popleft()
