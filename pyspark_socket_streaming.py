from pyspark.sql import SparkSession
import socket

server = socket.socket()
host =  socket.gethostbyname(socket.gethostname())

try:
    spark = SparkSession.builder.appName('boo').master('local[*]').getOrCreate()

    try:  
        socket_source_stream = spark \
        .readStream \
        .format('socket') \
        .option('host', f'{host}') \
        .option('port', '5011') \
        .option('includeTimestamp', True).load()
    except Exception as err:
        print(f'Error establishing spark socket stream : \n',err)
    else:
        print('-----\n Is spark streaming: ', socket_source_stream.isStreaming, '\n\n')   
        socket_source_stream.printSchema()

        socket_sink_stream = socket_source_stream.writeStream.queryName('sneeze')\
            .format('console')\
            .trigger(processingTime='2 second')\
            .start(truncate=False)
        socket_sink_stream.awaitTermination(30)         
    finally:
        print('\nStreaming Over.\n\n')

except Exception as err:
    print(f'\Error creating SparkSession: \n\n', err)

else:
    print('All went good.\n')

finally:
    spark.stop()
    print('SparkSession stopped!')
