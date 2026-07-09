"""Tests para el sistema de eventos de LINPRO."""

from linpro.core.events import EventBus, Event


class TestEvent:
    def test_dataclass_name(self):
        e = Event(name="test.event")
        assert e.name == "test.event"

    def test_dataclass_data_default(self):
        e = Event(name="test.event")
        assert e.data == {}

    def test_dataclass_data_personalizado(self):
        e = Event(name="test.event", data={"key": "value"})
        assert e.data == {"key": "value"}

    def test_dataclass_timestamp(self):
        from datetime import datetime
        e = Event(name="test.event")
        assert isinstance(e.timestamp, datetime)


class TestEventBus:
    def test_singleton(self):
        a = EventBus.get_instance()
        b = EventBus.get_instance()
        assert a is b

    def test_subscribe_y_publish_ejecuta_handler(self):
        bus = EventBus()
        resultados = []

        def handler(event):
            resultados.append(event.data)

        bus.subscribe("test.event", handler)
        bus.publish(Event(name="test.event", data={"msg": "hola"}))
        assert len(resultados) == 1
        assert resultados[0] == {"msg": "hola"}

    def test_unsubscribe_no_ejecuta_handler(self):
        bus = EventBus()
        resultados = []

        def handler(event):
            resultados.append(True)

        bus.subscribe("test.event", handler)
        bus.unsubscribe("test.event", handler)
        bus.publish(Event(name="test.event"))
        assert len(resultados) == 0

    def test_publish_sin_suscriptores_no_lanza_error(self):
        bus = EventBus()
        bus.publish(Event(name="event.sin.suscriptores"))

    def test_clear_elimina_handlers(self):
        bus = EventBus()
        resultados = []

        def handler(event):
            resultados.append(True)

        bus.subscribe("test.event", handler)
        bus.clear()
        bus.publish(Event(name="test.event"))
        assert len(resultados) == 0

    def test_suscripcion_multiple_al_mismo_evento(self):
        bus = EventBus()
        resultados = []

        def h1(event):
            resultados.append("h1")

        def h2(event):
            resultados.append("h2")

        bus.subscribe("multi", h1)
        bus.subscribe("multi", h2)
        bus.publish(Event(name="multi"))
        assert resultados == ["h1", "h2"]

    def test_unsubscribe_solo_elimina_handler_especifico(self):
        bus = EventBus()
        resultados = []

        def h1(event):
            resultados.append("h1")

        def h2(event):
            resultados.append("h2")

        bus.subscribe("multi", h1)
        bus.subscribe("multi", h2)
        bus.unsubscribe("multi", h1)
        bus.publish(Event(name="multi"))
        assert resultados == ["h2"]