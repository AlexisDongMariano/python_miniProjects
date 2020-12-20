from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Video(name={name}, views={views}, likes={likes})'


# db.create_all() # creates the database but should be executed once

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video is required', required=True)
video_put_args.add_argument('views', type=int, help='Views of the video is required', required=True)
video_put_args.add_argument('likes', type=int, help='Likes on the video is required', required=True)

# serialize the VideoModel instance so that it can be converted to JSON
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)  # the return values will be serialized with 'resource_fields'
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message='Video id already exists...')

        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)   # adds the object to the current database session
        db.session.commit() # commit the changes made in the session and make it permanent
        return video, 201

# videos = {}

# def abort_if_dont_exists(video_id):
#     '''abort the program if the video does not exists when GETting/DELETEing the video_id'''
#     if video_id not in videos.keys():
#         # returns error code 404 and the message
#         abort(404, message=f'video id: {video_id} does not exists...')

# def abort_if_exists(video_id):
#     '''abort the program if video does exists when PUTting the video_id'''
#     if video_id in videos:
#         # code 409 means already exists
#         abort(409, message=f"video id: {video_id} already exists...")
    

# class Video(Resource):
#     def get(self, video_id):
#         abort_if_dont_exists(video_id)
#         return videos[video_id]
    
#     def put(self, video_id):
#         abort_if_exists(video_id)
#         args = video_put_args.parse_args()
#         videos[video_id] = args
#         return videos[video_id], 201    # 201 means created, 200 means OK

#     def delete(self, video_id):
#         abort_if_dont_exists(video_id)
#         del videos[video_id]
#         return '', 204  # 204 means deleted successfully

api.add_resource(Video, '/video/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True)