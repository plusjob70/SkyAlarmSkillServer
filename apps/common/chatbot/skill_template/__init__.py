class Component:
    def __new__(cls, *args, **kwargs):
        cls_name = cls.__name__
        camelcase_cls = cls_name[0].lower() + cls_name[1:]
        return {camelcase_cls: kwargs}


class QuickReply(Component):
    ...


class Link(Component):
    ...


class Thumbnail(Component):
    ...


class CarouselHeader(Component):
    ...


class SimpleText(Component):
    ...


class SimpleImage(Component):
    ...


class BasicCard(Component):
    ...


class CommerceCard(Component):
    ...


class ListCard(Component):
    ...


class ItemCard(Component):
    ...


class Carousel(Component):
    ...


class ItemList(Component):
    ...


class Button(Component):
    def __new__(cls, *args, **kwargs):
        return kwargs


class Item:
    def __new__(cls, *args, **kwargs):
        return kwargs


class Obj:
    def __new__(cls, *args, **kwargs):
        return kwargs
