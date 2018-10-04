from flask import Flask,render_template,flash,redirect,session,logging,request,url_for
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from flask_mysqldb import MySQL
from functools import wraps

#debug decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu ekrana girebilmek için öncelikle girş yapmanız gereklidir..","danger")
            return redirect("/login")
    return decorated_function


#forum form
class forum1(Form):
    title = StringField("Başlık",validators=[validators.length(min = 4, max = 60,)])
    content = TextAreaField("Başlık İçeriği",validators=[validators.length(min = 9, max = 1000)])

#forum form
class makale1(Form):
    title = StringField("Makale başlık",validators=[validators.length(min = 4, max = 60,)])
    content = TextAreaField("Makale İçeriği",validators=[validators.length(min = 9, max = 1000)])

#yanıt form
class Yanıt(Form):
    yanıt = StringField("Yanıt ekleyin:")

#kullanıcı giriş arayüzü
class login1(Form):
    username = StringField("Kullanıcı adınız:")
    password = PasswordField("Parolanız")


#kayıt arayüzü
class register1(Form):
    name = StringField("İsim Soyisim",validators=[validators.length(min = 4, max = 14, message="İsminiz 4-14 haneli olabilir")])
    email = StringField("E-mail",validators=[validators.email(message=("Doğru mail girin."))])
    username = StringField("Kullanıcı adı",validators=[validators.length(min = 4, max = 15, message="Kullanıcı adınız 4-15 haneli olabilir")])
    password = PasswordField("Şifreniz",validators=[
        validators.data_required(message="Burayı boş bırakamazsınız"),
        validators.EqualTo(fieldname="confirm",message="Parolalar uyuşmuyor")
    ])
    
    
    
    
    confirm = PasswordField("Parola doğrulama")

app = Flask(__name__)

app.secret_key="msm"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "msm"
app.config["MYSQL_CURSORCLASS"] ="DictCursor"

mysql = MySQL(app) 

#ana ekran
@app.route("/")
def mainbase():
    return render_template("manage.html")

#kayıt ekranı
@app.route("/register", methods = ["GET","POST"])
def register():
    form = register1(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor()

        try:
            eylem = "Insert into datam(name,email,password,username) VALUES(%s,%s,%s,%s)"

            cursor.execute(eylem,(name,email,password,username))

            mysql.connection.commit()

        except:

            flash("kullanıcı adı ve ya eposta kullanılıyor","danger")

            return redirect("/register")

        cursor.close()

        flash("Başarıyla Kayıt Olundu...","success")

        return redirect("/login")

    else:

        return render_template("register.html",form = form)

#Bağış
@app.route("/donate")
def donate():
    return render_template("donate.html")

#hakkımızda
@app.route("/about")
def about_us():
    return render_template("hakkımızda.html")

#giriş ekranı
@app.route("/login",methods = ["GET","POST"])
def login():
    form = login1(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()
        eylem = "select * from datam where username = %s"
        result = cursor.execute(eylem,(username,))

        if result > 0:
            data = cursor.fetchone()
            real_p = data["password"]
            if real_p == password_entered:
                flash("Başarıyla giriş yapıldı","success")
                session["logged_in"] = True
                session["username"] = username

                return redirect("/")
            else:
                flash("Hatalı parola...","danger")
                return redirect("/login")

        else:
            flash("Böyle bir kullanıcı bulunmuyor..","danger")
            return redirect("/login")


    return render_template("login.html",form = form)

#çıkış
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

#forum anasayfa
@app.route("/forum")
def forum():
    cursor = mysql.connection.cursor()

    eylem = "select * from soru"

    result = cursor.execute(eylem)

    sorular = cursor.fetchall()

    if result > 0:
        return render_template("soru/soru.html",sorular=sorular)
    else:
        return render_template("soru/soru.html")


#forum soru içeriği
@app.route("/forum_baslik/<string:id>",methods = ["GET","POST"])
@login_required
def forumsoru(id):
    cursor = mysql.connection.cursor()
    eylem = "Select * from soru where id = %s"
    result = cursor.execute(eylem,(id,))
    form = Yanıt(request.form)


    if result > 0:
        soru = cursor.fetchone()

        if request.method == "POST":

            yanıt = form.yanıt.data

            eylem2 = "Insert into yanıt(yanıt,id,author) values(%s,%s,%s) "

            cursor.execute(eylem2,(yanıt,id,session["username"]))


            flash("Başarıyla yanıt eklendi...","success")


            mysql.connection.commit()

            cursor.close()

            return redirect("/forum_baslik/{}".format(id))

        else:

            cursor = mysql.connection.cursor()
            eylem6 = "Select * from yanıt where id = %s"
            result3 = cursor.execute(eylem6,(id))
            yanıtlar = cursor.fetchall()


            if result3 > 0:
                return render_template("soru/forumsoru.html",soru = soru,form = form,yanıtlar = yanıtlar)
            else:              
                return render_template("soru/forumsoru.html",soru = soru,form = form)
            cursor.close()
    else:
        return render_template("soru/forumsoru.html")


#soru ekleme
@app.route("/baslikekle",methods = ["GET","POST"])
@login_required
def soruekle():
    form = forum1(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data

        cursor = mysql.connection.cursor()

        eylem = " Insert into soru(title,content,author) values(%s,%s,%s)"

        cursor.execute(eylem,(title,content,session["username"]))

        mysql.connection.commit()

        cursor.close()

        flash("Başlığınız başarı ile eklendi","success")

        return redirect("/forum")

    return render_template("soru/soruekle.html",form=form)

#başlıklarım bölümü
@app.route("/basliklarim")
@login_required
def sorularım():
    cursor = mysql.connection.cursor()

    eylem = "Select * From soru where author = %s"

    result = cursor.execute(eylem,(session["username"],))

    if result > 0:
        sorular = cursor.fetchall()
        return render_template("soru/sorularım.html",sorular = sorular)
    else:
        return render_template("soru/sorularım.html")

#makaleler
@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()

    eylem = "select * from makale"

    result = cursor.execute(eylem)

    makaleler = cursor.fetchall()

    if result > 0:
        return render_template("articles.html",makaleler=makaleler)
    else:
        return render_template("articles.html")



#silme
@login_required
@app.route("/delete/<string:id>")
def delete(id):
    cursor = mysql.connection.cursor()
    eylem = "Select * from soru where author = %s and id = %s"
    result = cursor.execute(eylem,(session["username"],id))
    if result > 0:
        eylem2 = "Delete from soru where id = %s"
        eylem5 = "Delete from yanıt where id = %s"
        cursor.execute(eylem2,(id,))
        cursor.execute(eylem5,(id,))
        mysql.connection.commit()
        return redirect("/basliklarim")
    else:
        flash("Bu başlığı silmeye yetkiniz yok ya da başlık mevcut değil..","danger")
        return redirect("/")

#makale güncelleme
@login_required
@app.route("/edit/<string:id>",methods = ["GET","POST"])
def update(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        eylem = "Select * from soru where author = %s and id = %s"
        result = cursor.execute(eylem,(session["username"],id))
        if result == 0:
            flash("Bu eylemigerçekleştirmeye yetkiniz yok ya da başlık mevcut değil..","danger")
            return redirect("/")
        else:
            baslik = cursor.fetchone()
            form = forum1()

            form.title.data = baslik["title"]
            form.content.data = baslik["content"]
            return render_template("update.html",form = form)
    else:
        form = forum1(request.form)

        newtitle = form.title.data
        newcontent = form.content.data

        eylem2 = "Update soru Set title = %s,content = %s where id = %s"

        cursor = mysql.connection.cursor()

        cursor.execute(eylem2,(newtitle,newcontent,id))

        mysql.connection.commit()

        flash("Başlık başarı ile güncellendi","success")

        return redirect("/basliklarim")

#soru arama
@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "GET":
        return redirect("/forum")
    else:
        keyword = request.form.get("keyword")

        cursor = mysql.connection.cursor()

        eylem4 = "Select * from soru where title like '%" + keyword + "%' "

        result = cursor.execute(eylem4)

        if result == 0:
            flash("Aranan anahtara uygun başlık bulunamadı","warning")
            return redirect("/forum")
        else:
            sorular = cursor.fetchall()

            return render_template("soru/soru.html", sorular=sorular)

#makale ekleme
@app.route("/article_add_author_extend_123456",methods = ["GET","POST"])
@login_required
def yazıekle():
    form = makale1(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data

        cursor = mysql.connection.cursor()

        eylem = " Insert into makale(title,content,author) values(%s,%s,%s)"

        cursor.execute(eylem,(title,content,session["username"]))

        mysql.connection.commit()

        cursor.close()

        flash("Makaleniz başarı ile eklendi","success")

        return redirect("/articles")

    return render_template("makale_ekleme.html",form=form)

#makale içi görme
@app.route("/makale/<string:id>")
def makale_sonuç(id):
    cursor = mysql.connection.cursor()
    eylem = "Select * from makale where id = %s"
    result = cursor.execute(eylem,(id,))

    if result > 0:
        makale = cursor.fetchone()
        mysql.connection.commit()
        cursor.close()
        return render_template("makale_sonuç.html",makale=makale)
    else:            
        return render_template("makale_sonuç.html")

@app.route("/communication")
def communication():
    return render_template("iletişim.html")

@app.route("/writers")
def writers():
    return render_template("writers.html")


if __name__ == "__main__":
    app.run(debug = True)
