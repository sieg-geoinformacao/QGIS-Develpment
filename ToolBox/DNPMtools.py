# -*- coding: utf-8 -*-
import sys


from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingParameterString,
                       QgsProcessingParameterEnum ,
                       QgsProject,
                       QgsVectorLayer
                       
                       
                    )
import qgis.utils
import processing
import os
import zipfile


class DNPMData(QgsProcessingAlgorithm):
    """
    Ferramenta utlizada para donwload dos dados do DNPM
    """
    nmEstado = 'INPUT'
    estados = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MT','MG','PA',
                    'PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE',"Brasil"]
    OUTPUT = 'OUTPUT'
    
    
    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DNPMData()

    def name(self):
        """
        Retorna no nome do algoritmo para usar no QGIS.
        """
        return 'dnmp'


    def displayName(self):
        """
        Retorna o nome da ferramenta.
        """
        return self.tr('Download processos DNPM')
    
    def group(self):
        """
        Retorna o nome do grupo no script
        """
        return self.tr('Agência Nacional de Pesquisa Mineral')

    def groupId(self):
        
        return 'Agência Nacional de Pesquisa Mineral'

    
    def shortHelpString(self):
        """
       Retorna a ajuda da ferramenta
        """
        return self.tr("This tools is used to donwload DNPM process")

    #Inital tools
    def initAlgorithm(self, config=None):
        
       #Parameter
       #nome do estado
        self.addParameter(
            QgsProcessingParameterEnum(
                self.nmEstado,
                self.tr('Nome do Estado'),
                self.estados
            )
        )
      
              
       #Parametro de saida
        self.addParameter(
            QgsProcessingParameterFolderDestination(
                self.OUTPUT,
                #'D:/IPCA', optional=True, fileFilter='Todos os arquivos (*.*)', createByDefault=True, defaultValue=None
                self.tr('Pasta de saida')
                
                
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        #Nome do Estado
        nomeEstado = self.parameterAsEnum(parameters,self.nmEstado,context)
        estado = self.estados[nomeEstado]

        #Url
        url = 'http://sigmine.dnpm.gov.br/sirgas2000/'
        urlcompleto = url + estado +'.zip'

        #Folder de saida
        folderOutput = os.path.join(self.parameterAsString(parameters,self.OUTPUT,context),estado +'.zip')
        
        #Parametros da ferramenta
        parametros_tools = {
                'URL': urlcompleto,
                'OUTPUT':folderOutput
        }
        
        dnpmOutFile = processing.run("native:filedownloader",
                                                    parametros_tools,
                                                    context=context,
                                                    feedback=feedback
                                                    )

        descompatando = zipfile.ZipFile(folderOutput).extractall(os.path.dirname(folderOutput))
        
        #Criando o VectorLayer
        shapefile = os.path.join(self.parameterAsString(parameters,self.OUTPUT,context),estado +'.shp')
                   
        return {self.OUTPUT:shapefile}
