from tienda.models import Region, Comuna

datos = {
    "Arica y Parinacota": ["Arica", "Camarones", "Putre", "General Lagos"],
    "Tarapacá": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"],
    "Antofagasta": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama"],
    "Atacama": ["Copiapó", "Caldera", "Tierra Amarilla", "Vallenar", "Freirina", "Huasco", "Alto del Carmen"],
    "Coquimbo": ["La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paihuano", "Vicuña", "Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"],
    "Valparaíso": ["Valparaíso", "Viña del Mar", "Concón", "Quintero", "Puchuncaví", "Casablanca", "Juan Fernández", "Quillota", "La Calera", "Hijuelas", "La Cruz", "Nogales", "San Antonio", "Cartagena", "El Quisco", "El Tabo", "San Sebastián", "Algarrobo", "Santo Domingo"],
    "Metropolitana de Santiago": ["Santiago", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "Puente Alto", "San Bernardo", "Calera de Tango", "Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor", "Colina", "Lampa", "Til Til", "Pirque", "San José de Maipo", "Buin", "Paine"],
    "Libertador General Bernardo O'Higgins": ["Rancagua", "Machalí", "Graneros", "Rengo", "San Fernando", "Santa Cruz", "Pichilemu", "San Vicente", "Requínoa", "Doñihue", "Coinco"],
    "Maule": ["Talca", "Curicó", "Linares", "Parral", "San Javier", "Cauquenes", "Constitución", "Molina", "Teno"],
    "Ñuble": ["Chillán", "Chillán Viejo", "San Carlos", "Coihueco", "Bulnes", "Quillón", "Yungay"],
    "Biobío": ["Concepción", "Talcahuano", "San Pedro de la Paz", "Hualpén", "Chiguayante", "Coronel", "Lota", "Tomé", "Penco", "Hualqui", "Florida", "Los Ángeles", "Nacimiento", "Mulchén", "Cabrero", "Laja", "San Rosendo", "Yumbel"],
    "La Araucanía": ["Temuco", "Padre Las Casas", "Villarrica", "Pucón", "Angol", "Victoria", "Lautaro", "Nueva Imperial", "Freire", "Gorbea", "Carahue", "Toltén"],
    "Los Ríos": ["Valdivia", "La Unión", "Río Bueno", "Paillaco", "Lanco", "Panguipulli", "Mariquina", "Futrono", "Lago Ranco"],
    "Los Lagos": ["Puerto Montt", "Puerto Varas", "Osorno", "Castro", "Ancud", "Chonchi", "Fresia", "Frutillar", "Llanquihue", "Maullín", "Calbuco", "Quellón", "Quemchi", "Dalcahue", "Puyehue", "Purranque", "Río Negro"],
    "Aysén del General Carlos Ibáñez del Campo": ["Coyhaique", "Puerto Aysén", "Chile Chico", "Cochrane"],
    "Magallanes y de la Antártica Chilena": ["Punta Arenas", "Puerto Natales", "Porvenir", "Puerto Williams"]
}

def run():
    for nombre_region, comunas in datos.items():
        region, _ = Region.objects.get_or_create(nombre=nombre_region)
        for nombre_comuna in comunas:
            Comuna.objects.get_or_create(nombre=nombre_comuna, region=region)
    print("✅ Regiones y comunas cargadas correctamente.")
