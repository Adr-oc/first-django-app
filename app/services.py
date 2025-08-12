import requests
from django.conf import settings
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class LocationIQService:
    """Servicio para interactuar con la API de LocationIQ"""
    
    def __init__(self):
        self.api_key = settings.LOCATIONIQ_API_KEY
        self.base_url = settings.LOCATIONIQ_BASE_URL
        
    def get_address_from_coordinates(self, latitude, longitude):
        """
        Obtiene la dirección a partir de coordenadas usando reverse geocoding
        
        Args:
            latitude (float): Latitud
            longitude (float): Longitud
            
        Returns:
            dict: Información de la dirección o None si hay error
        """
        if not self.api_key:
            logger.error("LocationIQ API key no configurada")
            return None
            
        try:
            url = f"{self.base_url}/reverse.php"
            params = {
                'key': self.api_key,
                'lat': latitude,
                'lon': longitude,
                'format': 'json',
                'accept-language': 'es'  # Para obtener direcciones en español
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extraer información relevante
            address_info = {
                'display_name': data.get('display_name', ''),
                'address': {
                    'road': data.get('address', {}).get('road', ''),
                    'house_number': data.get('address', {}).get('house_number', ''),
                    'suburb': data.get('address', {}).get('suburb', ''),
                    'city': data.get('address', {}).get('city', ''),
                    'state': data.get('address', {}).get('state', ''),
                    'country': data.get('address', {}).get('country', ''),
                    'postcode': data.get('address', {}).get('postcode', '')
                }
            }
            
            # Crear dirección legible
            address_parts = []
            if address_info['address']['house_number']:
                address_parts.append(address_info['address']['house_number'])
            if address_info['address']['road']:
                address_parts.append(address_info['address']['road'])
            if address_info['address']['suburb']:
                address_parts.append(address_info['address']['suburb'])
            if address_info['address']['city']:
                address_parts.append(address_info['address']['city'])
            if address_info['address']['state']:
                address_parts.append(address_info['address']['state'])
            if address_info['address']['postcode']:
                address_parts.append(address_info['address']['postcode'])
            if address_info['address']['country']:
                address_parts.append(address_info['address']['country'])
                
            address_info['formatted_address'] = ', '.join(address_parts)
            
            return address_info
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la API de LocationIQ: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado en LocationIQ: {str(e)}")
            return None
    
    def is_api_key_valid(self):
        """Verifica si la API key es válida"""
        return bool(self.api_key and self.api_key != 'your_api_key_here')
