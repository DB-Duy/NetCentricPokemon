SERVER_IP = "172.25.35.210"

ACTION_ATTACK = "attack"
ACTION_SWITCH = "switch"
ACTION_SURRENDER = "surrender"
ACTION_ACCEPT = "accept"
ACTION_DECLINE = "decline"

PACKETTYPE_PLAYER_ACTION = "player_action"
PACKETTYPE_POLLING = "polling packet"
PACKETTYPE_HANDSHAKE = "handshake"
PACKETTYPE_SERVER_RESPONSE = "server_response"

BATTLESTATE_AWAIT_PLAYERS = 'waiting for players'
BATTLESTATE_AWAIT_ACTION = 'waiting for actions'
BATTLESTATE_AWAIT_OTHER_PLAYER_ACTION = 'waiting for other player actions'
BATTLESTATE_EXECUTING_ACTION = 'executing player actions'
