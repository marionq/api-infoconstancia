import fitz
import base64

class GetInfoPdf:

    def get_info_pdf (self, string_base64):
        
        with open(string_base64, "rb") as pdfFile:
            encodedString = base64.b64encode(pdfFile.read())
        
        string_base64_2 = str(encodedString)
        string_base64_3 = string_base64_2.replace("b'", "")
        string_base64_4 = string_base64_3.replace("'", "")
        
        try:
            file_64_decode = base64.b64decode(string_base64_4) 
            file_result = open('sample_decoded.pdf', 'wb') 
            file_result.write(file_64_decode)        

            documento = fitz.open("sample_decoded.pdf")
            """print(documento.load_page(0).get_text().replace("\t", " "))"""
            paginas = documento.page_count
            page1 = documento.load_page(0)
            page2 = documento.load_page(1)
            """print(page.get_text())"""
            texto1 = page1.get_text()
            texto2 = page2.get_text()
            
            validacion = texto1[20:51]
            response_get_inf = [] 
            
            if validacion == "CEDULA DE IDENTIFICACION FISCAL":                                
        
                posicion_rfc = texto1.find('RFC')
                rfc = texto1[posicion_rfc + 5 : posicion_rfc + 4 + 13]

                razon_social_posicion_inicio = (texto1.find('Registro Federal de Contribuyentes')) + 34
                razon_social_posicion_fin = (texto1.find('Nombre, denominación o razón'))
                razon_social = texto1[razon_social_posicion_inicio : razon_social_posicion_fin]
                razon_social_format = razon_social.replace("\n", "")

                posicion_cp_inicio = texto1.find('Código Postal') + 14
                posicion_cp_fin = texto1.find('Tipo de Vialidad')
                cp = texto1[posicion_cp_inicio : posicion_cp_fin]
                cp_format = cp.replace("\n", "")

                posicion_regimen_inicio = texto2.find('Regímenes:')
                posicion_regimen_fin = texto2.find('Obligaciones:')
                regimen_sin_formato = texto2[posicion_regimen_inicio : posicion_regimen_fin]
                posicion_regimen_inicio = regimen_sin_formato.find('Fecha Fin') + 9
                regimen_sin_formato = regimen_sin_formato[posicion_regimen_inicio : len(regimen_sin_formato) - 11]
                regimen = regimen_sin_formato.replace("\n", "")
                
                fecha_emision_posicion_inicio = (texto1.find('Lugar y Fecha de Emisión')) + 24
                fecha_emision_posicion_fin = (texto1.find('Datos de Identificación del Contribuyente') + 41)
                fecha_emision_tr1 = texto1[fecha_emision_posicion_inicio : fecha_emision_posicion_fin]
                fecha_emision_tr2_inicio = (fecha_emision_tr1.find(' A ')) + 3
                fecha_emision_tr2_fin = (fecha_emision_tr1.find(rfc))
                fecha_emision_sin_formato = fecha_emision_tr1[fecha_emision_tr2_inicio : fecha_emision_tr2_fin]
                fecha_emision = fecha_emision_sin_formato.replace("\n", "")
                
                print(f'RFC: {rfc}')
                print(f'Razón Social: {razon_social_format}')
                print(f'Código Postal: {cp_format}')
                print(f'Régimen: {regimen}')
                       
                response_get_inf.append({
                            'rfc': rfc,
                            'razon_social': razon_social_format,
                            'codigo_postal': cp_format,
                            'regimen': regimen,
                            'fecha_emicion': fecha_emision
                        })

                return response_get_inf
            else:
                response_get_inf.append({
                            'msg': 'archivo invalido'
                        })
                return response_get_inf
    
        except Exception as ex:
            return ex
