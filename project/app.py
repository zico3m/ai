from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# تحميل البيانات
users = pd.read_csv("users.csv")
articles = pd.read_csv("articles.csv")
news = pd.read_csv("news.csv")
interactions = pd.read_csv("interactions.csv")
comments = pd.read_csv("comments.csv")

# المجلد لحفظ الصور
if not os.path.exists("static"):
    os.mkdir("static")

@app.route("/")
def index():
    # مثال: أول 10 مستخدمين تفاعلًا
    user_interactions = interactions.groupby("user_id").size().reset_index(name="total_interactions")
    user_interactions = user_interactions.merge(users[["user_id","username"]], on="user_id")
    top_users = user_interactions.sort_values("total_interactions", ascending=False).head(10)

    # رسم بياني (أكثر المستخدمين تفاعلًا)
    plt.figure(figsize=(8,5))
    plt.barh(top_users["username"], top_users["total_interactions"], color="skyblue")
    plt.xlabel("عدد التفاعلات")
    plt.ylabel("المستخدم")
    plt.title("أكثر 10 مستخدمين تفاعلًا")
    plt.tight_layout()
    chart_path = "static/top_users.png"
    plt.savefig(chart_path)
    plt.close()

    # عدد المقالات والأخبار
    content_counts = {
        "المقالات": articles["content_id"].nunique(),
        "الأخبار": news["content_id"].nunique()
    }

    # عدد التعليقات الجيدة والمسيئة
    abusive_table = comments["is_abusive"].value_counts().reset_index()
    abusive_table.columns = ["type", "total_comments"]
    abusive_table["type"] = abusive_table["type"].replace({True:"مسيئة", False:"جيدة"})

    return render_template("index.html",
                           top_users=top_users.to_html(classes="table table-bordered", index=False),
                           content_counts=content_counts,
                           abusive_table=abusive_table.to_html(classes="table table-striped", index=False),
                           chart_path=chart_path)

if __name__ == "__main__":
    app.run(debug=True)
