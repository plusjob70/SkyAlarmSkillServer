class Outputs:
    def __init__(self, outputs):
        self.outputs = outputs


class QuickReplies:
    def __init__(self, label, action, message_text, block_id, extra):
        ...


class Template:
    def __init__(self, outputs, quick_replies=None):
        self.outputs: list[Outputs] = outputs

        if quick_replies is not None:
            self.quickReplies: list[QuickReplies] = quick_replies


class SimpleText:
    ...


class SimpleImage:
    ...
