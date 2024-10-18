import ds
import env
from pyflink.common import Types
from pyflink.datastream.window import Time, WindowAssigner, TumblingProcessingTimeWindows
from pyflink.common.time import Time
from pyflink.datastream.functions import WindowFunction

# Função para calcular a média
class AverageWindowFunction(WindowFunction):
    def apply(self, window, key, inputs, collector):
        count = 0
        total = 0.0
        for value in inputs:
            total += float(value)
            count += 1
        collector.collect(total / count)

# Definir uma janela de 30 segundos (ajuste para teste)
windowed_stream = ds \
    .map(lambda value: float(value)) \
    .window_all(TumblingProcessingTimeWindows.of(Time.seconds(30))) \
    .apply(AverageWindowFunction(), Types.FLOAT())

# Imprimir a média calculada
windowed_stream.print()

# Executar o job com a janela de média
env.execute("Kafka Consumer Job with Window")
