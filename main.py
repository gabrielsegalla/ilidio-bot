from twitch_chat_irc import twitch_chat_irc


connection = twitch_chat_irc.TwitchChatIRC()

users = []
users_banned = []

channel = "segalla_"

def moderate(message):
    context_msg = message.get('message').split(" ")
    if '!ban' in context_msg[0]:
        message_to_send = '👀'
        if context_msg[1].lower() not in users_banned:
            user = {
                'name' : context_msg[1],
                'votes': 0 
            }
            users.append(user)
            users_banned.append(context_msg[1].lower())
            message_to_send = 'Se liga @{} ai mais 10 votos e vc leva um timeout'.format(context_msg[1])
        else:
            result = next(
                (obj for obj in users if obj.get('name') == context_msg[1]),
                None
            )
            index = users.index(result)
            
            if result.get('votes') + 1 is 10:
                message_to_send = '/ban {} 300'.format(result.get('name'))
                users[index] = {
                    'name' : result.get('name'),
                    'votes':   0
                }
            else:
                message_to_send = 'Mais {} votos e o @{} leva um timeout'.format(10 - (result.get('votes') + 1), result.get('name'))
                users[index] = {
                    'name' : result.get('name'),
                    'votes':   result.get('votes') + 1
                }
                
            
        
        connection.send(channel, message_to_send)

connection.listen(channel, on_message=moderate)