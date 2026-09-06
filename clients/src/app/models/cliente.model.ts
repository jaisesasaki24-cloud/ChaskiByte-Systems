export interface Cliente {
  id?: number;
  tipoDocumento: 'DNI' | 'RUC';
  numeroDocumento: string;
  nombres?: string;
  apellidos?: string;
  razonSocial?: string;
  direccion?: string;
  email?: string;
  telefono?: string;
  estado?: string;
  condicionContribuyente?: string;
}

export interface ConsultaReniecResponse {
  fuente: string;
  dni: string;
  nombres: string;
  apellidoPaterno: string;
  apellidoMaterno: string;
  nombreCompleto: string;
  digitoVerificador: string;
  estadoDni: string;
  departamento: string;
  provincia: string;
  distrito: string;
}

export interface ConsultaSunatResponse {
  fuente: string;
  ruc: string;
  razonSocial: string;
  estadoContribuyente: string;
  condicionDomicilio: string;
  tipoContribuyente: string;
  direccionFiscal: string;
  emisionElectronica: string[];
  afectoIGV: boolean;
}
