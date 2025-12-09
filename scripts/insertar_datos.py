import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.dao.usuario_dao import UsuarioDAO
dao = UsuarioDAO()

usuarios = [
    ('LAZZARINI ADRIAN OMAR', '20342079653', '20342079653', 'Ramolaz2025', None),
    ('LAZZARINI HECTOR CESAR', '20140914089', '20140914089', 'Ramolaz2025', None),
    ('LAZZARINI&LAZZARINI S.R.L.', '20146327401', '30714395609', 'Ramolaz2024', None),
    ('PAROLA TERESA MARGARITA', '27111480864', '27111480864', 'Ramolaz2025', None),
    ('GOMEZ MIRTHA ANGELICA', '27140916973', '27140916973', 'Ramolaz2024', None),
    ('PALAZZI ALICIA BEATRIZ', '27132612671', '27132612671', 'Ramolaz2025', None),
    ('CEJAS VITO MIGUEL', '23111487529', '23111487529', 'Ramolaz2025', None),
    ('BARSLUND SILVIA ANDREA', '27283916869', '27283916869', 'Cardiologia17', None),
    ('DE MADARIAGA GLADYS MABEL', '27130099179', '27130099179', 'Ramolaz2025', None),
    ('LAZZARINI JULIO OMAR', '20146327401', '20146327401', 'Ramolaz2024', None),
    ('GALEANO ADRIAN YVO JAVIER', '20348428692', '20348428692', 'Ramolaz2025', None),
    ('PEREDO MONICA ISABEL', '27106230450', '27106230450', 'Ramolaz2025', None),
    ('ALVAREZ MARIELA NOEMI', '27332250812', '27332250812', 'Ramolaz2025', '3322Marie'),
    ('VALLEJO GUSTAVO GERMAN', '20324892649', '20324892649', 'Ramolaz2025', 'Eliott7526'),
]

for nombre, cuit, cuit_retenido, password, password_atp in usuarios:
    dao.insertar(nombre, cuit, cuit_retenido, password, password_atp)

print("Datos insertados correctamente.")
