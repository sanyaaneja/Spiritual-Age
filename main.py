#"male", "others" is not saved in csv
import flet as ft
import datetime
import csv
"""DEFAULT_FLET_PATH = ''  # or 'ui/path'
DEFAULT_FLET_PORT = 8502"""

Lst = ["", "", "", "", "", "", ""]
txt_name = ["", "", "", "", "", "", ""]

i = 0
current_question = 0
lst = []
#lst = [7,4,3,4,3,3,3,4,4,2,3,3,3,3,0]
score = 0.0

# Read questions from the csv file
with open('questions.csv', newline='', encoding='utf-8') as f:
  reader = csv.DictReader(f)
  questions = list(reader)
  for k1 in range(len(questions) - 1):
    count = -1
    for i1, j1 in questions[k1].items():
      if j1 != '':
        count += 1

    lst.append(int(count / 2))

  lst.append(0)


def main(page: ft.Page):
  page.theme_mode = "dark"
  page.window_height = 755
  page.window_width = 500
  page.horizontal_alignment = 'center'
  page.vertical_alignment = ft.MainAxisAlignment.CENTER
  page.scroll = 'always'
  page.update()

  page.title = "Know your spiritual age"

  def on_keyboard(e: ft.KeyboardEvent):
        page.add(
            ft.Text(
                f"Key: {e.key}"
            )
        )
        if (e.key == "Enter"):
           lambda _: page.go("/0")
  
  def btn_click(e):
    #page.add(txt_name)

    #Lst = []
    for i in range(len(l)):
      if not txt_name[i].value:
        txt_name[i].error_text = "Please enter your " + l[i]
      else:
        name = txt_name[i].value
        if i == 0:
          if all(chr.isalpha() or chr.isspace() for chr in name) == True:
            #if name.isalpha() == True:
            #Lst.append(name)
            Lst[i] = name
            txt_name[i].error_text = ""
          else:
            txt_name[i].error_text = "Please enter a valid name"

        elif i == 1:
          if name.isdigit() == True and len(name) == 10:
            #Lst.append(name)
            Lst[i] = name
            txt_name[i].error_text = ""
          else:
            txt_name[i].error_text = "Please enter a valid phone number"
        elif i == 2:  # added if txt_name[i] != None:    else .. Gender"

          if txt_name[i].value != None:
            txt_name[i].error_text = ""
          else:
            txt_name[i].error_text = None

        elif i == 3:  #added isdigit() ..()
          if name.isdigit() == True and int(name) >= 10 and int(name) <= 100:
            Lst[i] = name
            txt_name[i].error_text = ""
          else:
            txt_name[i].error_text = "Please enter a valid age"

        elif i == 5 or i == 4:

          Lst[i] = name
          txt_name[i].error_text = ""

        elif i == 6:
          page.on_keyboard_event = on_keyboard
        
          while True:
            try:
              day, month, year = name.split('/')
              datetime.datetime(int(year), int(month), int(day))
              txt_name[i].error_text = ""
              Lst[i] = name
              break

            except ValueError:
              txt_name[i].error_text = "Please enter a valid date"

      page.update()

    flag = True
    for i in range(len(l)):
      if txt_name[i].error_text != "":
        flag = False
        btn_click

    if flag == True:
      page.on_route_change = route_change
      page.on_view_pop = view_pop
      page.go(page.route)

  page.title = "Start Page"

  l = [
    "name", "phone number", "gender (M/F)", "age (between 10 and 100)",
    "qualification/profession", "address",
    "Brahm Gyan Deeksha date(DD/MM/YYYY)"
  ]

  for j in range(len(l)):
    if j == 2:
      txt_name[j] = ft.Dropdown(
        label="Your " + l[j],
        width=400,
        options=[
          ft.dropdown.Option("Female"),
          ft.dropdown.Option("Male"),
          ft.dropdown.Option("Other"),
        ],
      )

    else:
      txt_name[j] = ft.TextField(label="Your " + l[j], width=400)

  def route_change(route):
    global current_question

    page.views.clear()

    pb = ft.ProgressBar(width=510)

    def button_clicked(e):
      page.go("/" + str(e))
      global score
      if e.control.data in choices:
        ans = choices.index(e.control.data)
        score += float(myScores[ans])
        Lst.append(f'{chr(ord("A") + ans)}')

    choices = [
      questions[current_question][f'Choice {chr(ord("A") + i + j)}']
      for j in range(lst[current_question])
    ]
    myScores = [
      questions[current_question][f'Score {chr(ord("A") + i + j)}']
      for j in range(lst[current_question])
    ]

    dlg = ft.AlertDialog(title=ft.Text("Your spiritual age is " + str(score) +
                                       "!"),
                         on_dismiss=lambda e: print("Dialog dismissed!"))

    def open_dlg(e):
      page.dialog = dlg
      dlg.open = True
      page.update()

    page.views.append(
      ft.View(
        "/",
        [ft.ElevatedButton("Start Quiz", on_click=lambda _: page.go("/0"))],
      ))

    page.views.append(
      ft.View(
        "/0",
        [
          ft.Row([ft.Text(""), pb]),
          ft.AppBar(center_title = True, title=ft.Text("Know your spiritual age"),
                    bgcolor=ft.colors.SURFACE_VARIANT),
          # Question label
          ft.Text(questions[current_question]['Question'], text_align = ft.TextAlign.CENTER),
          *[
            ft.ElevatedButton(
              text=choice, on_click=button_clicked, data=choice)
            for choice in choices
          ],
        ],
      ))

    num_questions = len(questions)
    for k in range(1, num_questions + 1):
      pb.value = current_question / (num_questions - 2)
      choices = [
        questions[current_question][f'Choice {chr(ord("A") + i + j)}']
        for j in range(lst[current_question])
      ]

      if page.route == "/" + str(k):
        page.views.append(
          ft.View(
            "/" + str(k),
            [
              ft.AppBar(center_title = True, title=ft.Text("Know your spiritual age"),
                        bgcolor=ft.colors.SURFACE_VARIANT),
              # Question label
              ft.Text(questions[current_question]['Question']),
              *[
                ft.ElevatedButton(
                  text=choice, on_click=button_clicked, data=choice)
                for choice in choices
              ],
              ft.Column([ft.Text(""), pb])
            ],
          ))
    current_question += 1
    if current_question == num_questions:
      page.views.append(
        ft.View(
          "/" + str(num_questions),
          [
            ft.AppBar(center_title = True, title=ft.Text("Know your spiritual age"),
                      bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Text("Jai Maharaj Ji"),
          ],
        ))

      if score > 0:
        Lst.append(score)  # add current date and time
        with open('answers.csv', mode='a', newline='', encoding='utf-8') as f:
          Write = csv.writer(f)
          Write.writerow(Lst)
      open_dlg(None)

    page.update()

  def view_pop(view):
    page.views.pop()
    top_view = page.views[-1]
    page.go(top_view.route)

  b = ft.ElevatedButton(text='Start Quiz', on_click=btn_click)
  page.add(txt_name[0], txt_name[1], txt_name[2], txt_name[3], txt_name[4],
           txt_name[5], txt_name[6], b)


"""if __name__ == "__main__":
    flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
    app(name=flet_path, target=main, view=None, port=flet_port)"""

#app(target=main, view=WEB_BROWSER, port = 56940)
ft.app(main, view=ft.AppView.WEB_BROWSER)
