from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

EMOCIONES = ['Feliz', 'Triste', 'Relajado', 'Estresado', 'Aburrido', 'Ansioso']

ZONAS = ['Centro', 'Poblado', 'Laureles', 'Belén', 'Envigado']

LUGARES = [
    {
        'id': 1,
        'nombre': 'Pub Rock Medellin',
        'tipo': 'Bar',
        'zona': 'Poblado',
        'emociones': ['Feliz', 'Aburrido'],
        'descripcion': 'Bar de rock con bandas en vivo, ideal para disfrutar música de los 80 y 90',
        'descripcion_larga': 'Icónico bar de rock ubicado en el corazón del Parque Lleras. Cuenta con bandas en vivo que interpretan los mejores clásicos del rock de los años 80 y 90 en español e inglés. El ambiente es perfecto para disfrutar de buena música en vivo, cervezas artesanales y comida pub. Las bandas interactúan con el público y aceptan peticiones, creando una experiencia única cada noche. Ideal para amantes del rock que buscan un lugar auténtico con excelente sonido y ambiente festivo.',
        'direccion': 'Carrera 37A #8-12, Parque Lleras',
        'coordenadas': '6.207420475658616, -75.56761109042117',
        'imagen': 'pub rock.jpg'
    },
    {
        'id': 2,
        'nombre': 'Pueblito Paisa',
        'tipo': 'Mirador',
        'zona': 'Belén',
        'emociones': ['Feliz', 'Relajado'],
        'descripcion': 'Réplica de pueblo antioqueño en la cima del Cerro Nutibara con vista panorámica',
        'descripcion_larga': 'Réplica arquitectónica de un tradicional pueblo antioqueño del siglo XX ubicado en la cima del Cerro Nutibara, a 80 metros sobre el nivel de la ciudad. Cuenta con una plaza central de piedra, iglesia, casa cural, alcaldía y tiendas de artesanías. Desde su ubicación privilegiada se obtiene una vista panorámica de 360 grados de todo el Valle de Aburrá. El recorrido incluye senderos ecológicos con más de 100 especies de flora y 56 de fauna. Entrada gratuita todos los días desde las 5:30 a.m. hasta las 10:00 p.m. Perfecto para conocer la cultura paisa y tomar fotografías impresionantes de la ciudad.',
        'direccion': 'Calle 30A #55-64, Cerro Nutibara',
        'coordenadas': '6.236334708611071, -75.5802694457505',
        'imagen': 'pueblito paisa.jpg'
    },
    {
        'id': 3,
        'nombre': 'Sala de Despecho',
        'tipo': 'Bar',
        'zona': 'Poblado',
        'emociones': ['Triste', 'Feliz', 'Aburrido'],
        'descripcion': 'Bar temático de despecho con música popular colombiana',
        'descripcion_larga': 'Bar temático especializado en música de despecho y popular colombiana. El lugar está decorado con frases de canciones románticas y cuenta con una ambientación nostálgica perfecta para cantar a todo pulmón éxitos de Diomedes Díaz, Darío Gómez y otros grandes del género. Ofrece cócteles con nombres inspirados en canciones populares y un menú de comida típica colombiana. El ambiente festivo y descomplicado hace que sea el lugar ideal para un plan con amigos donde la música popular y el buen humor son protagonistas. Los viernes y sábados hay presentaciones en vivo de músicos locales.',
        'direccion': 'Carrera 35 #8-46',
        'coordenadas': '6.20806992750064, -75.5646692311093',
        'imagen': 'sala de despecho.jpg'
    },
    {
        'id': 4,
        'nombre': 'Salón Málaga',
        'tipo': 'Discoteca',
        'zona': 'Centro',
        'emociones': ['Feliz', 'Aburrido'],
        'descripcion': 'Discoteca clásica de Medellín con música variada y ambiente festivo',
        'descripcion_larga': 'Discoteca clásica y emblemática de Medellín con más de 40 años de historia. Es conocida por su pista de baile amplia, luces de neón y música variada que incluye salsa, merengue, vallenato, música popular y los mejores éxitos bailables. El lugar mantiene un ambiente tradicional pero festivo, siendo uno de los sitios más concurridos del centro de la ciudad los fines de semana. Cuenta con varias barras, zonas VIP y un sistema de sonido de alta calidad. Es el lugar perfecto para bailar toda la noche y disfrutar de un ambiente auténticamente paisa. Abre de jueves a domingo desde las 8:00 p.m.',
        'direccion': 'Carrera 51 #45-80',
        'coordenadas': '6.2465648624923675, -75.56969861128604',
        'imagen': 'salon malaga.webp'
    },
    {
        'id': 5,
        'nombre': 'Teatro Águila Descalza',
        'tipo': 'Teatro',
        'zona': 'Laureles',
        'emociones': ['Feliz', 'Triste', 'Relajado', 'Estresado', 'Aburrido', 'Ansioso'],
        'descripcion': 'Teatro independiente con obras contemporáneas y experimentales',
        'descripcion_larga': 'Teatro independiente y alternativo dedicado a las artes escénicas contemporáneas y experimentales. Fundado en 1996, es un espacio cultural que promueve nuevas formas de expresión teatral con montajes innovadores, obras de dramaturgia contemporánea y performances de artistas locales e internacionales. La sala íntima de 80 personas crea una conexión especial entre actores y espectadores. Además de obras de teatro, ofrece talleres de actuación, improvisación y otras disciplinas artísticas. El lugar también funciona como punto de encuentro para la comunidad teatral y artística de Medellín. Programación variada toda la semana.',
        'direccion': 'Calle 45 #70-39',
        'coordenadas': '6.254792397326555, -75.56067535789069',
        'imagen': 'teatro aguila descalza.webp'
    },
    {
        'id': 6,
        'nombre': 'Teatro Metropolitano',
        'tipo': 'Teatro',
        'zona': 'Centro',
        'emociones': ['Feliz', 'Triste', 'Relajado'],
        'descripcion': 'Teatro principal de Medellín con programación cultural variada',
        'descripcion_larga': 'Teatro principal de Medellín inaugurado en 1987, considerado una joya arquitectónica de la ciudad. Con capacidad para 1.676 espectadores, cuenta con excelente acústica y tecnología de punta para espectáculos de gran formato. Presenta una programación diversa que incluye ópera, ballet, conciertos sinfónicos, teatro clásico y contemporáneo, danza y festivales internacionales. La Orquesta Filarmónica de Medellín tiene aquí su sede principal. El edificio combina elementos modernos con detalles coloniales, creando un ambiente elegante y sofisticado. Es sede de importantes eventos culturales como el Festival Internacional de Poesía y el Festival Internacional de Tango.',
        'direccion': 'Calle 41 #57-30',
        'coordenadas': '6.243059919316701, -75.57716639694729',
        'imagen': 'teatro metropolitano.jpg'
    },
    {
        'id': 7,
        'nombre': 'Teatro Pablo Tobón Uribe',
        'tipo': 'Teatro',
        'zona': 'Centro',
        'emociones': ['Feliz', 'Triste', 'Relajado', 'Aburrido'],
        'descripcion': 'Teatro con excelente acústica, programación de ópera, ballet y conciertos',
        'descripcion_larga': 'Uno de los teatros más importantes de Colombia, reconocido por su arquitectura moderna y excelente acústica. Inaugurado en 1967, tiene capacidad para 1.150 espectadores distribuidos en platea, primer y segundo balcón. Es sede de la Orquesta Sinfónica EAFIT y presenta una programación de alto nivel que incluye ópera, ballet clásico y contemporáneo, conciertos de música clásica, jazz y world music, además de producciones teatrales nacionales e internacionales. El teatro ofrece temporadas de abono y presenta artistas de talla mundial. Su ubicación céntrica y sus instalaciones modernas lo convierten en un referente cultural de la ciudad.',
        'direccion': 'Carrera 40 #51-24',
        'coordenadas': '6.247574248976651, -75.55929519482189',
        'imagen': 'teatro pablo tobon uribe.jpg'
    },
    {
        'id': 8,
        'nombre': 'Brutal',
        'tipo': 'Bar',
        'zona': 'Laureles',
        'emociones': ['Feliz', 'Aburrido'],
        'descripcion': 'Bar con ambiente urbano, música electrónica y cócteles artesanales',
        'descripcion_larga': 'Bar urbano y contemporáneo con un concepto moderno que fusiona el arte callejero con la cultura de los cócteles artesanales. El ambiente industrial-chic cuenta con murales de artistas locales, iluminación tenue y música electrónica seleccionada por DJs residentes. La carta de cócteles incluye creaciones originales con ingredientes locales y técnicas de mixología avanzada. También ofrece una selección de cervezas artesanales colombianas y destilados premium. El espacio tiene dos niveles, con una terraza en el segundo piso ideal para grupos. Los jueves presentan sets de música en vivo y los fines de semana DJs invitados. Popular entre el público joven y cosmopolita del Poblado.',
        'direccion': 'Carrera 37 #8A-32',
        'coordenadas': '6.245544936480212, -75.58937551752176',
        'imagen': 'brutal.jpg'
    },
    {
        'id': 9,
        'nombre': 'El Canalón',
        'tipo': 'Bar',
        'zona': 'Laureles',
        'emociones': ['Feliz', 'Relajado', 'Aburrido'],
        'descripcion': 'Bar de ambiente relajado con música en vivo y buena comida',
        'descripcion_larga': 'Bar-restaurante de ambiente relajado y bohemio ubicado en el corazón del Poblado. Destaca por su arquitectura colonial adaptada con un patio central lleno de plantas y decoración vintage. Es famoso por su música en vivo de rock, jazz y blues con presentaciones de músicos locales e invitados especiales varias noches a la semana. El menú fusiona comida internacional con toques locales, destacando las hamburguesas gourmet, los tacos y las tablas de quesos. El ambiente tranquilo durante el día se transforma en una fiesta moderada por la noche. Cuenta con mesas al aire libre y espacios acogedores en el interior. Ideal para conversar, trabajar durante el día o disfrutar de buena música en la noche.',
        'direccion': 'Cq. 2 #47-101, Laureles - Estadio, Medellín, Laureles, Medellín, Antioquia, Colombia',
        'coordenadas': '6.245948866474926, -75.58850069650528',
        'imagen': 'canalon.jpeg'
    },
    {
        'id': 10,
        'nombre': 'Cocorollo',
        'tipo': 'Restaurante',
        'zona': 'Poblado',
        'emociones': ['Feliz', 'Relajado'],
        'descripcion': 'Restaurante de cocina caribeña con ambiente tropical',
        'descripcion_larga': 'Restaurante de cocina costeña y caribeña que trae los sabores del Caribe colombiano a Medellín. La decoración tropical con palmas, colores vibrantes y música de fondo caribeña transportan a los comensales a las playas del norte de Colombia. El menú incluye especialidades como la cazuela de mariscos, el pescado frito en salsa de coco, el arroz con chipi chipi y los patacones con hogao. También ofrece cócteles tropicales preparados con ron y frutas frescas. El ambiente festivo pero relajado es perfecto para almuerzos en grupo o cenas casuales. Los fines de semana hay música en vivo de vallenato y champeta, creando un ambiente alegre y familiar.',
        'direccion': 'Carrera 37 #8A-44',
        'coordenadas': '6.214647477955373, -75.5729510671657',
        'imagen': 'cocorollo.jpg'
    },
    {
        'id': 11,
        'nombre': 'Comuna 13',
        'tipo': 'Tour',
        'zona': 'Centro',
        'emociones': ['Feliz', 'Ansioso'],
        'descripcion': 'Tour por el arte urbano y escaleras eléctricas de la Comuna 13',
        'descripcion_larga': 'Tour guiado por una de las transformaciones urbanas más inspiradoras del mundo. La Comuna 13, antes conocida por su violencia, se ha convertido en un museo de arte urbano al aire libre con más de 200 grafitis que cuentan historias de resiliencia y esperanza. El recorrido incluye las famosas escaleras eléctricas (primeras de su tipo en Colombia), que facilitan la movilidad de los habitantes. Durante el tour, guías locales narran la historia del barrio, el conflicto armado y la transformación social. Se visitan miradores con vistas espectaculares de la ciudad y se interactúa con artistas urbanos y emprendedores locales. La experiencia incluye degustación de comida típica y productos artesanales. Tours disponibles todos los días con salidas cada hora desde las 9:00 a.m.',
        'direccion': 'Comuna 13, San Javier',
        'coordenadas': '6.247945136494773, -75.62199273026883',
        'imagen': 'comuna 13.avif'
    },
    {
        'id': 12,
        'nombre': 'Edificio Inteligente EPM',
        'tipo': 'Edificio',
        'zona': 'Centro',
        'emociones': ['Feliz', 'Relajado', 'Ansioso'],
        'descripcion': 'Edificio sostenible con museo interactivo sobre energía',
        'descripcion_larga': 'Edificio corporativo sostenible y futurista que es un referente de arquitectura verde en América Latina. Cuenta con certificación LEED Platinum y múltiples tecnologías de ahorro energético y gestión eficiente del agua. En el primer piso hay un museo interactivo gratuito sobre energía, sostenibilidad y servicios públicos, con exhibiciones interactivas que explican cómo funcionan las plantas de generación de energía, el ciclo del agua y las nuevas tecnologías renovables. El edificio tiene jardines verticales, techos verdes y sistemas de recolección de agua lluvia. Se ofrecen tours guiados gratuitos previa reserva que incluyen visita a las zonas sostenibles y al mirador del último piso. Un ejemplo de innovación arquitectónica y compromiso ambiental.',
        'direccion': 'Carrera 58 #42-125',
        'coordenadas': '6.24534472286482, -75.57763199414676',
        'imagen': 'edificio inteligente epm.webp'
    },
    {
        'id': 13,
        'nombre': 'El Social',
        'tipo': 'Café',
        'zona': 'Poblado',
        'emociones': ['Relajado', 'Feliz', 'Aburrido', 'Ansioso'],
        'descripcion': 'Café acogedor con terraza, ideal para trabajar o conversar',
        'descripcion_larga': 'Café acogedor y moderno con un ambiente tranquilo perfecto para trabajar, estudiar o reunirse con amigos. Cuenta con amplias mesas comunales, enchufes en cada mesa y excelente WiFi gratuito. La terraza al aire libre en el segundo piso está rodeada de plantas y ofrece una vista agradable del vecindario. Especializado en café de especialidad colombiano con métodos de preparación como chemex, v60 y aeropress. El menú incluye desayunos saludables, sándwiches gourmet, ensaladas frescas y una selección de postres caseros. También ofrece opciones veganas y vegetarianas. El ambiente es relajado durante el día, convirtiéndose en un bar de vinos y cócteles por la noche. Popular entre nómadas digitales, estudiantes y profesionales del Poblado.',
        'direccion': 'Carrera 36 #9-55',
        'coordenadas': '6.210355631392099, -75.56538753509999',
        'imagen': 'el social.jpg'
    },
    {
        'id': 14,
        'nombre': 'La Logia',
        'tipo': 'Bar',
        'zona': 'Laureles',
        'emociones': ['Relajado', 'Feliz'],
        'descripcion': 'Bar estiludo con cócteles clásicos y ambiente sofisticado',
        'descripcion_larga': 'Bar estilo speakeasy con concepto de barra escondida que recrea la atmósfera de los bares clandestinos de los años 20. La entrada discreta da paso a un ambiente íntimo con iluminación tenue, decoración vintage y música jazz de fondo. Los bartenders son expertos en coctelería clásica y preparan drinks personalizados según los gustos del cliente. La carta incluye cócteles clásicos como Old Fashioned, Negroni y Manhattan, así como creaciones de la casa con ingredientes premium. El lugar tiene capacidad limitada, creando una experiencia exclusiva y sofisticada. No hay música fuerte ni baile, el enfoque está en la conversación y en disfrutar de buenos tragos en un ambiente elegante. Requiere reserva los fines de semana.',
        'direccion': 'Carrera 37 #9-60',
        'coordenadas': '6.249935199936324, -75.5881261499643',
        'imagen': 'la logia.jpg'
    },
    {
        'id': 15,
        'nombre': 'Mamasita',
        'tipo': 'Restaurante',
        'zona': 'Poblado',
        'emociones': ['Feliz', 'Relajado', 'Triste'],
        'descripcion': 'Restaurante de cocina nacional con terraza al aire libre',
        'descripcion_larga': 'Restaurante de cocina colombiana e internacional con un ambiente moderno y acogedor. Destaca por su amplia terraza al aire libre rodeada de vegetación que crea un oasis en medio del bullicio del Poblado. El menú fusiona técnicas culinarias contemporáneas con ingredientes locales, ofreciendo desde platos tradicionales colombianos reinventados hasta propuestas internacionales. Especialidades incluyen los cortes de carne angus, pescados del Pacífico, risottos cremosos y una selección de ceviches. La carta de cócteles es variada y la selección de vinos nacionales e internacionales es amplia. El ambiente es casual-elegante, perfecto para almuerzos de negocios, cenas románticas o celebraciones familiares. Los domingos ofrecen brunch con música en vivo.',
        'direccion': 'Carrera 37 #8-63',
        'coordenadas': '6.2119485472539235, -75.57158972719742',
        'imagen': 'mamasita.png'
    },
    {
        'id': 16,
        'nombre': 'Melodía para Dos',
        'tipo': 'Cafe Bar',
        'zona': 'Laureles',
        'emociones': ['Relajado', 'Triste', 'Feliz'],
        'descripcion': 'Café romántico con música en vivo, perfecto para parejas y grupos de amigos',
        'descripcion_larga': 'Café romántico y nostálgico con un concepto musical único donde la melodía y el café se encuentran. El lugar está decorado con instrumentos musicales antiguos, vinilos en las paredes y una rocola con clásicos del bolero y baladas románticas. Es famoso por sus presentaciones de música en vivo de cantautores locales los fines de semana, donde se interpretan canciones de amor y desamor. El menú incluye cafés especiales, chocolates calientes artesanales, postres caseros y un toque de repostería francesa. También ofrece menú de cenas ligeras con opciones de fondue y tablas de quesos. El ambiente íntimo con luces bajas lo hace perfecto para citas románticas, aunque también es ideal para ir con amigos a disfrutar de buena música acústica. Las noches de micrófono abierto atraen a talento local.',
        'direccion': 'Carrera 35 #8-40',
        'coordenadas': '6.247807019421241, -75.58986186312411',
        'imagen': 'melodia para dos.jpg'
    },
    {
        'id': 17,
        'nombre': 'Miranda',
        'tipo': 'Restaurante',
        'zona': 'Poblado',
        'emociones': ['Feliz', 'Relajado'],
        'descripcion': 'Restaurante con cocina de autor y ambiente elegante',
        'descripcion_larga': 'Restaurante de alta cocina con propuesta de autor que combina técnicas culinarias vanguardistas con ingredientes colombianos de alta calidad. El chef propone un menú degustación de temporada que cambia cada tres meses, explorando los sabores de diferentes regiones de Colombia con presentaciones artísticas. El ambiente es elegante y minimalista, con una decoración contemporánea que resalta la arquitectura del espacio. Cuenta con una cava de vinos con más de 200 referencias nacionales e internacionales y un sommelier que ayuda a maridar cada plato. El servicio es impecable y la atención al detalle es evidente en cada aspecto de la experiencia. Ideal para ocasiones especiales, celebraciones importantes o para quienes buscan una experiencia gastronómica memorable. Requiere reserva con anticipación.',
        'direccion': 'Carrera 37A #10A-35',
        'coordenadas': '6.209934989698584, -75.56597510183909',
        'imagen': 'miranda.jpg'
    },
    {
        'id': 18,
        'nombre': 'Museo de Antioquia',
        'tipo': 'Museo',
        'zona': 'Centro',
        'emociones': ['Relajado', 'Aburrido', 'Feliz'],
        'descripcion': 'Museo con obras de Fernando Botero y arte colombiano',
        'descripcion_larga': 'Museo de arte más antiguo de Antioquia fundado en 1881, ubicado frente a la icónica Plaza Botero. Alberga la colección más grande de obras de Fernando Botero, incluyendo 108 pinturas y 22 esculturas donadas por el artista a su ciudad natal. Las exhibiciones abarcan desde arte precolombino y colonial hasta arte moderno y contemporáneo colombiano. El edificio histórico conocido como el Antiguo Palacio Municipal data de 1920 y es una joya arquitectónica. El museo ofrece exposiciones permanentes y temporales, talleres educativos, conferencias y eventos culturales. La tienda del museo tiene una excelente selección de libros de arte y artesanías locales. La cafetería ofrece un espacio tranquilo para descansar. Entrada general $18.000, estudiantes y adultos mayores con descuento. Domingos entrada gratuita.',
        'direccion': 'Carrera 52 #52-43',
        'coordenadas': '6.2525726940760595, -75.56814341370652',
        'imagen': 'museo de antioquia.jpg'
    },
    {
        'id': 19,
        'nombre': 'Museo de Arte Moderno',
        'tipo': 'Museo',
        'zona': 'Centro',
        'emociones': ['Relajado', 'Aburrido', 'Feliz'],
        'descripcion': 'Museo de arte contemporáneo con exposiciones temporales',
        'descripcion_larga': 'Museo dedicado al arte moderno y contemporáneo de Colombia y América Latina. Fundado en 1978, presenta una programación dinámica con exposiciones temporales de artistas nacionales e internacionales emergentes y consagrados. El edificio industrial restaurado ofrece amplias salas de exhibición con iluminación natural. Las colecciones exploran movimientos artísticos como el expresionismo, el arte conceptual, la instalación y los nuevos medios. Además de las exposiciones, el museo tiene una agenda activa de charlas con artistas, talleres de creación, proyecciones de cine y performances. La biblioteca especializada en arte moderno está abierta al público. El museo también administra el Parque de las Esculturas a orillas del río Medellín. Entrada $10.000, gratis los miércoles.',
        'direccion': 'Carrera 44 #19A-100',
        'coordenadas': '6.223801725903923, -75.57379377842102',
        'imagen': 'museo de arte moderno.jpg'
    },
    {
        'id': 20,
        'nombre': 'Museo El Castillo',
        'tipo': 'Museo',
        'zona': 'Poblado',
        'emociones': ['Relajado', 'Feliz'],
        'descripcion': 'Castillo con jardines franceses y colección de arte europeo',
        'descripcion_larga': 'Majestuoso castillo de estilo gótico medieval francés construido en 1930, rodeado de jardines franceses declarados Bien de Interés Cultural. El castillo-museo alberga una colección de arte europeo, porcelanas, vitrales, muebles antiguos y objetos decorativos de los siglos XVIII y XIX. Los jardines de 8.000 metros cuadrados con diseño francés formal incluyen fuentes, esculturas, laberintos verdes y zonas de contemplación. El lugar ofrece recorridos guiados por el interior del castillo y los jardines, conciertos de música clásica en la terraza, exposiciones de arte temporal y eventos culturales. Es un lugar popular para sesiones fotográficas de bodas y eventos privados. La cafetería del museo sirve té, café y postres en un ambiente elegante con vista a los jardines. Entrada $15.000, incluye recorrido guiado.',
        'direccion': 'Calle 9 Sur #32-269',
        'coordenadas': '6.190170579057772, -75.56930132823703',
        'imagen': 'museo el castillo.png'
    },
    {
        'id': 21,
        'nombre': 'Parque Arví',
        'tipo': 'Parque',
        'zona': 'Envigado',
        'emociones': ['Feliz', 'Relajado', 'Ansioso', 'Estresado'],
        'descripcion': 'Parque natural con senderos ecológicos y mercado campesino',
        'descripcion_larga': 'Parque natural de 16.000 hectáreas ubicado en la zona montañosa al oriente de Medellín. Se accede mediante el Metrocable línea L, un recorrido escénico de 20 minutos sobre el bosque que ofrece vistas espectaculares del valle. El parque cuenta con más de 54 kilómetros de senderos ecológicos señalizados para caminatas de diferentes niveles de dificultad, desde paseos familiares hasta rutas de trekking exigente. Los senderos atraviesan bosques de niebla, quebradas y antiguos caminos de arrieros. El parque alberga 186 especies de aves, lo que lo convierte en un paraíso para el avistamiento. Los fines de semana funciona el Mercado Agroecológico Campesino donde productores locales venden frutas, verduras, lácteos y artesanías. También hay zonas de camping, áreas de picnic y restaurantes con comida típica. Entrada al parque gratuita, costo del Metrocable aparte.',
        'direccion': 'Santa Elena, vía Metrocable línea L',
        'coordenadas': '6.2816972329254765, -75.49830334334287',
        'imagen': 'parque arvi.webp'
    },
    {
        'id': 22,
        'nombre': 'Parque Explora',
        'tipo': 'Museo',
        'zona': 'Centro',
        'emociones': ['Feliz', 'Aburrido', 'Triste'],
        'descripcion': 'Museo interactivo de ciencia y tecnología con acuario',
        'descripcion_larga': 'Museo interactivo de ciencia y tecnología más grande de América Latina con más de 300 experiencias interactivas distribuidas en varias salas temáticas. Las exhibiciones permanentes incluyen física, biología, química, robótica, anatomía humana y sostenibilidad ambiental. Los visitantes pueden tocar, experimentar y aprender de manera lúdica sobre conceptos científicos. El acuario de agua dulce es el más grande de Sudamérica con 30 acuarios que representan ecosistemas colombianos, incluyendo el Amazonas y el Orinoco. El planetario digital ofrece proyecciones inmersivas sobre astronomía y el cosmos. El vivario exhibe serpientes, ranas y otras especies de reptiles y anfibios nativos. Hay talleres de robótica, laboratorios de química y experiencias de realidad virtual. Ideal para familias con niños. Entrada adultos $30.000, niños $23.000. Paquetes combinados disponibles.',
        'direccion': 'Carrera 52 #73-75',
        'coordenadas': '6.270102386898919, -75.5653028904359',
        'imagen': 'parque explora.webp'
    },
    {
        'id': 23,
        'nombre': 'Parque Norte',
        'tipo': 'Parque',
        'zona': 'Centro',
        'emociones': ['Feliz', 'Aburrido', 'Estresado', 'Ansioso'],
        'descripcion': 'Parque de diversiones con juegos mecánicos y atracciones',
        'descripcion_larga': 'Parque de atracciones mecánicas con más de 50 años de historia, siendo el favorito de varias generaciones de paisas. Cuenta con más de 30 juegos mecánicos que incluyen montañas rusas, carros chocones, castillo del terror, rueda de la fortuna, barco vikingo y juegos acuáticos. La zona infantil tiene juegos adaptados para los más pequeños. El parque también ofrece shows y presentaciones artísticas en temporadas especiales como Halloween y Navidad. Las extensas zonas verdes con árboles centenarios son perfectas para hacer picnic. Hay múltiples kioscos de comida con opciones de comida rápida, helados y algodón de azúcar. El parque organiza eventos temáticos, conciertos y festivales durante todo el año. Es un lugar nostálgico para adultos y emocionante para niños. Entrada $27.000 con acceso a todos los juegos. Abierto todos los días.',
        'direccion': 'Calle 67 #53-108',
        'coordenadas': '6.27219265544621, -75.56574277273134',
        'imagen': 'parque norte.jpg'
    },
    {
        'id': 24,
        'nombre': 'Pequeño Teatro',
        'tipo': 'Teatro',
        'zona': 'Laureles',
        'emociones': ['Relajado', 'Feliz', 'Triste'],
        'descripcion': 'Teatro íntimo con obras de teatro experimental y café bar',
        'descripcion_larga': 'Teatro independiente íntimo con sala de 100 butacas que ofrece una programación alternativa y experimental. Fundado hace más de 20 años, es un espacio cultural que promueve las artes escénicas contemporáneas con obras de autores colombianos y latinoamericanos. La programación incluye teatro, danza contemporánea, monólogos, stand-up comedy y performances multimedia. El teatro también funciona como escuela de actuación con talleres permanentes para todas las edades. El café-bar en el lobby es un punto de encuentro para artistas y amantes del teatro donde se realizan tertulias culturales y lecturas dramatizadas. El ambiente bohemio y alternativo atrae a un público que busca propuestas artísticas diferentes. Los viernes tienen noches de microteatro con obras cortas experimentales. Precios accesibles, entradas desde $15.000.',
        'direccion': 'Carrera 42 #43-71',
        'coordenadas': '6.2476914355980036, -75.56110633276305',
        'imagen': 'pequeño teatro.png'
    },
    {
        'id': 25,
        'nombre': 'Planetario de Medellín',
        'tipo': 'Museo',
        'zona': 'Centro',
        'emociones': ['Relajado', 'Aburrido', 'Feliz'],
        'descripcion': 'Planetario con proyecciones en domo y exposiciones astronómicas',
        'descripcion_larga': 'Centro de ciencia y astronomía con un moderno planetario digital que proyecta el universo en un domo de 20 metros de diámetro con capacidad para 300 personas. Las proyecciones inmersivas transportan a los visitantes a través del sistema solar, galaxias lejanas y fenómenos astronómicos. El museo cuenta con salas de exhibición permanente sobre la conquista espacial, las misiones Apollo, telescopios históricos y meteoritos reales. Las exhibiciones interactivas explican conceptos de física, gravedad, luz y el funcionamiento del universo. El observatorio en el techo permite observaciones astronómicas nocturnas con telescopios profesionales guiados por astrónomos (eventos especiales programados). Se ofrecen talleres de astronomía para niños y adultos, charlas con científicos y proyecciones especiales en fechas astronómicas importantes como eclipses y lluvias de meteoros. Entrada adultos $12.000, incluye proyección en el domo.',
        'direccion': 'Carrera 52 #71-117',
        'coordenadas': '6.269356287204752, -75.56527398672522',
        'imagen': 'planetario.jpg'
    }
]


CALIFICACIONES = []


@app.route('/')
def inicio():
    return render_template('inicio.html')


@app.route('/seleccion-emocion')
def seleccion_emocion():
    return render_template('seleccion_emocion.html', 
                         emociones=EMOCIONES,
                         zonas=ZONAS)


@app.route('/resultados')
def resultados():
    emocion = request.args.get('emocion')
    zona = request.args.get('zona')

    lugares_filtrados = []
    for lugar in LUGARES:
        if emocion in lugar['emociones']:
            if not zona or zona == 'Cualquier zona' or lugar['zona'] == zona:
                lugares_filtrados.append(lugar)
    
    return render_template('resultados.html',
                         lugares=lugares_filtrados,
                         emocion=emocion,
                         zona=zona)


@app.route('/detalle/<int:id_lugar>')
def detalle_lugar(id_lugar):
    lugar = None
    for l in LUGARES:
        if l['id'] == id_lugar:
            lugar = l
            break
    
    emocion_inicial = request.args.get('emocion', 'Feliz')
    
    return render_template('detalle_lugar.html',
                         lugar=lugar,
                         emocion_inicial=emocion_inicial,
                         emociones=EMOCIONES)


@app.route('/detalle/<int:id_lugar>', methods=['POST'])
def guardar_calificacion(id_lugar):
    lugar = None
    for l in LUGARES:
        if l['id'] == id_lugar:
            lugar = l
            break
    
    calificacion = {
        'nombre_lugar': lugar['nombre'],
        'emocion_antes': request.form.get('emocion_antes'),
        'emocion_despues': request.form.get('emocion_despues'),
        'calificacion': int(request.form.get('calificacion')),
        'comentario': request.form.get('comentario'),
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    
    CALIFICACIONES.append(calificacion)
    
    emocion = request.args.get('emocion', 'Feliz')
    zona = request.args.get('zona', 'Cualquier zona')
    return redirect(url_for('resultados', emocion=emocion, zona=zona))


@app.route('/panel-vendedor')
def panel_vendedor():
    return render_template('panel_vendedor.html',
                         calificaciones=CALIFICACIONES)


if __name__ == '__main__':
    print('MoodMap Medellín en: http://localhost:5000')
    app.run(debug=True, port=5000)
