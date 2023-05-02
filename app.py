from flask import Flask, request
from flask import jsonify
import py_eureka_client.eureka_client as eureka_client
from flask_zipkin import Zipkin

from GetInfoPdf import GetInfoPdf

eureka_client.init(eureka_server="http://localhost:8761/eureka",
                   app_name="api-infoconstancia",
                   instance_port=8082)

# app Flask
app = Flask(__name__)

zipkin = Zipkin(app, sample_rate=100)
app.config['ZIPKIN_DSN'] = "http://10.14.102.132:9411/"

@app.route('/autofin/v1/infoconstancia', methods = ['POST'])
def prueba():
    try:
        request_get_info = request.json
        get_info = GetInfoPdf()
        string_base64 = request_get_info['image_base64']
        info_pdf = get_info.get_info_pdf(string_base64)

        return (info_pdf)
    except Exception as ex:
        return ex

def pagina_no_encontrada(error):
    return "<h1>La página a la que intentas acceder no existe....</h1>", 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(port=8082)
    app.run(host='0.0.0.0', debug=False)