Сайт оценки еды - RateThisFood
Описание: 

Это сайт, написанный на python с применением HTML и CSS, на котором можно выставить свое блюдо, кратко его описать(состав, способ подачи и т.д.), оценить его вкус, вид и блюда других пользователей, и узнать, совпадают ли ваши вкусы в еде с мнением большинства.

ТЗ

На сайте должно быть:
1. Страница регистрации
2. Страница входа
3. Страница для создания своего блюда
4. Лента с блюдами пользователей, где можно узнать о составе блюда, его оценку, поставить ему оценку
5. На странице с лентой должна быть кнопка создания своего блюда

Также для работы сайта должно быть:
1. Базы данных пользователей и еды на движке SQL
   Поля баз данных:
  1.1 Пользователи: id, пользователь, email
  1.2 Блюда: id, название, описание, пользователь, который создал этот пост, среднее арифметическое оценки блюда, изображение блюда
3. Связь между этими базами
4. Роуты, созданные с применением модуля flask: login, registration - отвечают за регистрацию и вход, main_page - страница, куда попадает пользователь после входа с блюдами, add_dish - страница для добавления блюда
