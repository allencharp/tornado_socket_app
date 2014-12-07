#coding=utf8
import tornado.ioloop
import tornado.web
import tornado.websocket

clients = []
buffers = []

#diff12
class IndexHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self, request):
		request.render("index.html")

class SocketChatHandler(tornado.websocket.WebSocketHandler):
	def open(self, *args):
		print("open", "WebSocketChatHandler")
		clients.append(self)

	def on_message(self, message):
		print message
		for client in clients:
			client.write_message(message)
	
	def on_close(self):
		clients.remove(self)


class UploadHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("upload.html")


class SocketUploadHandler(tornado.websocket.WebSocketHandler):
	
	def open(self, *args):
		pass

	def on_message(self, message):
		if buffers == []:
			print "start"
			buffers.append(message)
		else:
			buffers.append(message)
			import os
			file_path = os.path.dirname(__file__) + buffers[0]
			print file_path
			bin_file = open(file_path, 'wb')
			bin_file.write(buffers[1])
			bin_file.close()
			buffers.pop()
			buffers.pop()

	def on_close(self):
		pass


app = tornado.web.Application([(r'/chat', SocketChatHandler),
							(r'/upload', UploadHandler),
							(r'/socket_upload', SocketUploadHandler),
							(r'/', IndexHandler)],
							debug=True)
app.listen(8005)
tornado.ioloop.IOLoop.instance().start()
