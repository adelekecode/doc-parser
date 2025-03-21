from marshmallow import Schema, fields, validate

class SlideSchema(Schema):
    slide_number = fields.Integer(required=True)
    title = fields.String(allow_none=True)
    content = fields.String(allow_none=True)
    has_images = fields.Boolean(default=False)
    has_charts = fields.Boolean(default=False)

class DocumentSchema(Schema):
    document_id = fields.String(required=True)
    original_filename = fields.String(required=True)
    file_path = fields.String(required=True)
    file_type = fields.String(required=True, validate=validate.OneOf(['pdf', 'pptx']))
    upload_timestamp = fields.DateTime(required=True)
    total_slides = fields.Integer(required=True)
    slides = fields.List(fields.Nested(SlideSchema))
    metadata = fields.Dict()
