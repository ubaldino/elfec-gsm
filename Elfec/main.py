#!/usr/bin/python2

#encoding:utf-8
__author__ = 'ubaldino'
__copyright__ = "...."

from optparse import OptionParser
from serial.tools import list_ports
import wx , os , time , serial


class Validate_Numeric( wx.PyValidator ):
	def __init__( Self ):
		wx.PyValidator.__init__( Self )
		Self.Bind( wx.EVT_TEXT , Self.On_Text_Change )
	
	def Clone( Self ):
		return Validate_Numeric()

	def On_Text_Change( Self , Event ):
		TextCtrl = Self.GetWindow()
		Text = TextCtrl.GetValue()
		if Text.isdigit() or Text == "":
			TextCtrl.SetBackgroundColour( "White" )
		else :
			TextCtrl.SetBackgroundColour( "Pink" )
		Event.Skip()

class Validate_Text( wx.PyValidator ):
	def __init__( Self ):
		wx.PyValidator.__init__( Self )
		Self.Bind( wx.EVT_TEXT , Self.On_Text_Change )
	
	def Clone( Self ):
		return Validate_Text()

	def On_Text_Change( Self , Event ):
		TextCtrl = Self.GetWindow()
		Text = TextCtrl.GetValue()
		if not Text.isdigit() or Text == "":
			TextCtrl.SetBackgroundColour( "White" )
		else :
			TextCtrl.SetBackgroundColour( "Pink" )
		Event.Skip()

class Main( wx.Frame ):
	def __init__(self):
		wx.Frame.__init__( self, None, -1, 'Elfec 1.0', size=( 850 , 600 ) )
		self.icon = wx.Icon( os.path.dirname( os.path.dirname(__file__) ) + '\\Elfec\\resources\\elfec.ico' , wx.BITMAP_TYPE_ICO )
		self.SetIcon( self.icon )
		self.panel = wx.Panel( self , -1 )
		self.count_conect = 0
		self.puerto_serial = None


		btn_buscar = wx.Button( self.panel , label='Buscar', pos=( 40 , 520 ))
		btn_conectar = wx.Button( self.panel , label='Conectar', pos=( 430 , 520 ))
		btn_desconectar = wx.Button( self.panel , label='Desconectar', pos=( 510 , 520 ) )
		btn_verificar = wx.Button( self.panel , label='Verificar', pos=( 640 , 520 ) )


        #### Text fomularios ######
		## cambiar de numeros
		self.lbl_telefonos = wx.StaticText( self.panel , label="Numeros Telefonicos", pos=( 80 , 40 ) )
		self.txt_telf1 = wx.TextCtrl( self.panel , value="Telefono 1" , style=wx.TE_CENTRE , pos=( 40 , 60 ) ,  validator=Validate_Numeric() )
		self.txt_telf1.SetMaxLength(8)
		self.txt_telf2 = wx.TextCtrl( self.panel , value="Telefono 2" , style=wx.TE_CENTRE , pos=( 40 , 90 ) , validator=Validate_Numeric() )
		self.txt_telf2.SetMaxLength(8)
		self.txt_telf3 = wx.TextCtrl( self.panel , value="Telefono 3" , style=wx.TE_CENTRE , pos=( 40 , 120 ) , validator=Validate_Numeric() )
		self.txt_telf3.SetMaxLength(8)
		
		btn_telf1 = wx.Button( self.panel , label='Telefono 1', pos=( 155 , 60 ) )
		btn_telf2 = wx.Button( self.panel , label='Telefono 2', pos=( 155 , 90 ) )
		btn_telf3 = wx.Button( self.panel , label='Telefono 3', pos=( 155 , 120 ) )


		## cambiar de numeros
		#self.lbl_tiempo = wx.StaticText( self.panel , label="Tiempo en segundos", pos=( 70 , 190 ) )
		#self.txt_tiempo = wx.TextCtrl( self.panel , value="Segundos" , style=wx.TE_CENTRE , pos=( 40 , 210 ) , validator=Validate_Numeric() )
		#self.lbl_tiempo = wx.StaticText( self.panel , label="Tiempo de ciclo de mensajes", pos=( 40 , 240 ) )
		#btn_tiempo = wx.Button( self.panel , label='Tiempo', pos=(	 150 , 210 ) )
		#btn_tiempo.Bind( wx.EVT_BUTTON , self.tiempo )
		
		## mensajes de activacion
		self.lbl_activacion = wx.StaticText( self.panel , label="Mensaje de activacion", pos=( 350 , 40 ) )
		self.txt_actv1 = wx.TextCtrl( self.panel , value="cerrar" , style=wx.TE_CENTRE , pos=( 320 , 60 ) ,  validator=Validate_Text() )
		self.txt_actv1.SetMaxLength( 6 )
		self.txt_actv2 = wx.TextCtrl( self.panel , value="abrir" , style=wx.TE_CENTRE , pos=( 320 , 90 ) , validator=Validate_Text() )
		self.txt_actv2.SetMaxLength( 6 )
		self.txt_actv3 = wx.TextCtrl( self.panel , value="reset" , style=wx.TE_CENTRE , pos=( 320 , 120 ) , validator=Validate_Text() )
		self.txt_actv3.SetMaxLength( 6 )

		btn_actv1 = wx.Button( self.panel , label='Salida 1', pos=( 430 , 60 ) )
		btn_actv2 = wx.Button( self.panel , label='Salida 2', pos=( 430 , 90 ) )
		btn_actv3 = wx.Button( self.panel , label='Salida 3', pos=( 430 , 120 ) )

		## Dispositivos de entrada
		self.lbl_entrada = wx.StaticText( self.panel , label="Dispositivos de entrada", pos=( 650 , 40 ) )
		self.txt_disp_ent1 = wx.TextCtrl( self.panel , value="cerrado" , style=wx.TE_CENTRE , pos=( 600 , 60 ) ,  validator=Validate_Text() )
		self.txt_disp_ent1.SetMaxLength(8)
		self.txt_disp_ent2 = wx.TextCtrl( self.panel , value="abierto" , style=wx.TE_CENTRE , pos=( 600 , 90 ) , validator=Validate_Text() )
		self.txt_disp_ent2.SetMaxLength(8)
		self.txt_disp_ent3 = wx.TextCtrl( self.panel , value="falla" , style=wx.TE_CENTRE , pos=( 600 , 120 ) , validator=Validate_Text() )
		self.txt_disp_ent3.SetMaxLength(8)
		self.txt_disp_ent4 = wx.TextCtrl( self.panel , value="reconex" , style=wx.TE_CENTRE , pos=( 600 , 150 ) , validator=Validate_Text() )
		self.txt_disp_ent4.SetMaxLength(8)

		btn_disp_ent1 = wx.Button( self.panel , label='Entrada 1', pos=( 720 , 60 ) )
		btn_disp_ent2 = wx.Button( self.panel , label='Entrada 2', pos=( 720 , 90 ) )
		btn_disp_ent3 = wx.Button( self.panel , label='Entrada 3', pos=( 720 , 120 ) )
		btn_disp_ent4 = wx.Button( self.panel , label='Entrada 4', pos=( 720 , 150 ) )

		#self.txt_telefon = wx.TextCtrl( self.panel , value="Numero telefonico" , style=wx.TE_CENTRE , pos=( 280 , 200 ) , validator=Validate_Numeric() )
		#btn_num_telf = wx.Button( self.panel , label='obtener numero', pos=( 280 , 225 ) )
		#btn_num_telf.Bind( wx.EVT_BUTTON , self.numtelf )


		#######  eventos #########
		# numeros
		btn_telf1.Bind( wx.EVT_BUTTON , self.telf1 )
		btn_telf2.Bind( wx.EVT_BUTTON , self.telf2 )
		btn_telf3.Bind( wx.EVT_BUTTON , self.telf3 )
		# mensajes activacion
		btn_actv1.Bind( wx.EVT_BUTTON , self.actv1 )
		btn_actv2.Bind( wx.EVT_BUTTON , self.actv2 )
		btn_actv3.Bind( wx.EVT_BUTTON , self.actv3 )
		# dispositovos entrada
		btn_disp_ent1.Bind( wx.EVT_BUTTON , self.ent1 )
		btn_disp_ent2.Bind( wx.EVT_BUTTON , self.ent2 )
		btn_disp_ent3.Bind( wx.EVT_BUTTON , self.ent3 )
		btn_disp_ent4.Bind( wx.EVT_BUTTON , self.ent4 )

		btn_buscar.Bind( wx.EVT_BUTTON , self.buscar_seriales )
		btn_conectar.Bind( wx.EVT_BUTTON , self.conectar_dispositivo )
		btn_desconectar.Bind( wx.EVT_BUTTON , self.desconectar_dispositivo )
		btn_verificar.Bind( wx.EVT_BUTTON , self.verificar_dispositivo )

		self.txt_result = wx.TextCtrl( self.panel , style=wx.TE_MULTILINE | wx.TE_AUTO_SCROLL , pos = ( 40 , 300 ) , size=( 760 , 160 ) )
		self.txt_result.SetBackgroundColour( wx.BLACK )
		self.txt_result.SetEditable(False)
		self.txt_result.SetForegroundColour( wx.RED )

		self.cb_devices = wx.ComboBox( self.panel , pos=( 140, 520 ), size=( 280, -1) , style=wx.CB_READONLY )
		#choices
		self.cb_devices.Bind( wx.EVT_COMBOBOX , self.OnSelect )


	def telf1( self , evt):
		if len( self.txt_telf1.GetValue() ) == 8:
			datos = self.mensaje_serial( str( self.txt_telf1.GetValue() ) + "*a\n" , 2 )
			self.txt_result.SetLabel( datos )
		else:

			self.txt_result.SetLabel( "Fallo en telefono 1" )
	
	def telf2( self , evt):
		if len( self.txt_telf2.GetValue() ) == 8:
			datos = self.mensaje_serial( str( self.txt_telf2.GetValue() ) + "*b\n" , 2 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en telefono 2" )

	def telf3( self , evt):
		if len( self.txt_telf3.GetValue() ) == 8:
			datos = self.mensaje_serial( str( self.txt_telf3.GetValue() ) + "*c\n" , 2 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en telefono 3" )
	# funciones de activacion
	def actv1( self , evt):
		if len( self.txt_actv1.GetValue() ) > 0:
			datos = self.mensaje_serial( str( self.txt_actv1.GetValue() ) + "*e\n" , 2.5 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en activacion 1" )

	def actv2( self , evt):
		if len( self.txt_actv2.GetValue() ) > 0:
			datos = self.mensaje_serial( str( self.txt_actv2.GetValue() ) + "*f\n" , 2.5 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en activacion 2" )

	def actv3( self , evt):
		if len( self.txt_actv3.GetValue() ) > 0:
			datos = self.mensaje_serial( str( self.txt_actv3.GetValue() ) + "*g\n" , 2.5 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en activacion 3" )
	#funciones de entrada
				
	def ent1( self , evt ):
		if len( self.txt_disp_ent1.GetValue() ) > 0:
			self.txt_result.SetLabel( str( self.txt_disp_ent1.GetValue() ) + "*h\n" )
			datos = self.mensaje_serial( str( self.txt_disp_ent1.GetValue() ) + "*h\n" , 3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en entrada 1" )

	def ent2( self , evt ):
		if len( self.txt_disp_ent2.GetValue() ) > 0:
			self.txt_result.SetLabel( str( self.txt_disp_ent2.GetValue() ) + "*i\n" )
			datos = self.mensaje_serial( str( self.txt_disp_ent2.GetValue() ) + "*i\n" , 3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en entrada 2" )

	def ent3( self , evt):
		if len( self.txt_disp_ent3.GetValue() ) > 0:
			self.txt_result.SetLabel( str( self.txt_disp_ent3.GetValue() ) + "*j\n" )
			datos = self.mensaje_serial( str( self.txt_disp_ent3.GetValue() ) + "*j\n" , 3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en entrada 3" )
	
	def ent4( self , evt):
		if len( self.txt_disp_ent4.GetValue() ) > 0:
			self.txt_result.SetLabel( str( self.txt_disp_ent4.GetValue() ) + "*k\n" )
			datos = self.mensaje_serial( str( self.txt_disp_ent4.GetValue() ) + "*k\n" , 3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "Fallo en telefono 3" )
	
	def numtelf( self , evt ):
		datos = self.mensaje_serial( "*l\n" , 0.5 )
		self.txt_result.SetLabel( datos + "\n" )
	
	def tiempo( self , evt ):
		if self.txt_tiempo.GetValue().isdigit():
			datos = self.mensaje_serial( hex( int( self.txt_tiempo.GetValue() ) )  + "*d\n" , 1.3 )
			self.txt_result.SetLabel( datos )
		else:
			self.txt_result.SetLabel( "No se pudo establecer el tempo \n ingrese numeros" )

	def buscar_seriales(self , evt ):
		self.devs_list = [] ; self.lista_devs = []
		self.txt_result.SetLabel( " | " )
		lista_disp = list( list_ports.comports() )
		for index in range( len( lista_disp ) ):
			self.devs_list.append( lista_disp[index][0] )
			self.lista_devs.append( lista_disp[index][1] )
			self.txt_result.SetLabel( self.txt_result.GetLabel() + lista_disp[index][0] + " | " )
			self.txt_result.SetSize( ( 760 , 160 ) )
		self.cb_devices.SetItems( self.lista_devs )
		self.cb_devices.SetSelection(0)
		self.cb_devices.SetFocus()


	def OnSelect( self, event ):
		self.item = self.cb_devices.GetSelection()
		print self.item

	def conectar_dispositivo( self , evt ):
		self.puerto_serial = serial.Serial( str( self.devs_list[ self.cb_devices.GetSelection() ] ) , 9600 )
		self.txt_result.SetLabel( "conectado a %s"%str( self.devs_list[ self.cb_devices.GetSelection() ] ) )
		self.txt_result.SetSize( ( 760 , 160 ) )

	def verificar_dispositivo( self , evt ):
		datos = self.mensaje_serial( "H\n" , 0.3 )
		self.txt_result.SetLabel( "\n"+datos + "\n"  )
		self.txt_result.SetSize( ( 760 , 160 ) )

	def desconectar_dispositivo( self , evt ):
		self.puerto_serial.close()
		self.txt_result.SetLabel( "Desconectado de : "+str( self.lista_devs[self.item] ) )
		self.txt_result.SetSize( ( 760 , 160 ) )

	def mensaje_serial( self , mensaje , delay ):
		#self.puerto_serial.flushInput()
		self.puerto_serial.write( mensaje )
		time.sleep( delay )
		return self.puerto_serial.read( self.puerto_serial.inWaiting() )

def main():
    app = wx.App(None)
    frame = Main()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
	main()
