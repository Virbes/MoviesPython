from flask import Flask
from flask_login import LoginManager

import views
from database import get_user

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')

    app.add_url_rule('/', view_func=views.home_page)
    app.add_url_rule('/login', view_func=views.login_page, methods=['GET', 'POST'])
    app.add_url_rule('/logout', view_func=views.logout_page)
    app.add_url_rule('/movies', view_func=views.movies_page, methods=['GET', 'POST'])
    app.add_url_rule('/movie/<int:movie_key>/edit', view_func=views.movie_edit_page, methods=['GET', 'POST'])
    app.add_url_rule('/movie/<int:movie_key>', view_func=views.movie_page)
    app.add_url_rule('/new-movie', view_func=views.movie_add_page, methods=['GET', 'POST'])
    app.add_url_rule('/profile', view_func=views.profile, methods=['GET', 'POST'])
    app.add_url_rule('/categories', view_func=views.categories, methods=['GET', 'POST'])
    app.add_url_rule('/categories/delete/<int:id_category>', view_func=views.delete_category, methods=['GET', 'POST'])
    app.add_url_rule('/manage-users', view_func=views.manage_users, methods=['GET', 'POST'])
    app.add_url_rule('/new-user', view_func=views.create_user, methods=['GET', 'POST'])
    app.add_url_rule('/users-edit', view_func=views.users_edit, methods=['GET', 'POST'])
    app.add_url_rule('/users-edit/<username>', view_func=views.edit_profile, methods=['GET', 'POST'])
    app.add_url_rule('/delete-users', view_func=views.delete_users, methods=['GET', 'POST'])
    app.add_url_rule('/delete-user/<int:id_user>', view_func=views.delete_user, methods=['GET', 'POST'])
    app.add_url_rule('/movie/<int:movie_key>/acquire', view_func=views.add_to_cart, methods=['GET', 'POST'])
    app.add_url_rule('/my-cart', view_func=views.my_cart, methods=['GET', 'POST'])
    app.add_url_rule('/delete/my-movie/<int:my_movie_key>', view_func=views.delete_my_movie, methods=['GET', 'POST'])

    app.add_url_rule('/payment', view_func=views.payment, methods=['GET', 'POST'])
    app.add_url_rule('/payment/cash', view_func=views.payment_cash, methods=['GET', 'POST'])
    app.add_url_rule('/ticket/<int:id_sale>', view_func=views.ticket, methods=['GET', 'POST'])

    app.add_url_rule('/my-shopping', view_func=views.my_shopping, methods=['GET', 'POST'])
    app.add_url_rule('/report-sales', view_func=views.report_sales, methods=['GET', 'POST'])

    app.add_url_rule('/about', view_func=views.about)

    lm.init_app(app)
    lm.login_view = 'login_page'

    return app


if __name__ == "__main__":
    _app = create_app()
    _app.run(host="0.0.0.0", port=8080)
