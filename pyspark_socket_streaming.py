from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split
import socket
import sys

server = socket.socket()
host =  socket.gethostbyname(socket.gethostname())

try:
    spark = SparkSession.builder.appName('socket_streaming').master('local[*]').getOrCreate()

    try:  
        socket_source_stream = spark \
        .readStream \
        .format('socket') \
        .option('host', f'{host}') \
        .option('port', '5011') \
        .option('includeTimestamp', True).load()
    except Exception as err:
        print(f'Error establishing spark socket stream : \n', sys.exc_info())
    else:
        print('\n----- Is spark streaming: ', socket_source_stream.isStreaming, '\n')   
        socket_source_stream.printSchema()
        try:
            stream_words_df = socket_source_stream.select(explode(split(socket_source_stream.value, " ")).alias("words"))
            stream_words_count_df = stream_words_df.groupBy("words").count()
        except Exception as err:
            print('Error in transformation:\n', sys.exc_info())
        else:
            socket_sink_stream = stream_words_count_df.writeStream.queryName('sink_socket_streaming')\
            .format('console')\
            .outputMode('update')\
            .start(truncate=False)
            socket_sink_stream.awaitTermination(55)    #.trigger(processingTime='1 second')\ "I removed this since processing power is hardware-dependant, since we ain't streaming much adding it neccesarily won't break our code, just make our terminal a little dirty"
        finally:
            pass      
    finally:
        print('\nStreaming Over.\n\n')

except Exception as err:
    print(f'\Error creating SparkSession: \n\n', sys.exc_info())

else:
    print('All went good.\n')

finally:
    spark.stop()
    print('SparkSession stopped!')

