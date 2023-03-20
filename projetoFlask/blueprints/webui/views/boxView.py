from flask import render_template, request, redirect, url_for
from projetoFlask.blueprints.webui.forms.BoxForm import BoxCreate
from flask_login import login_required, current_user
from projetoFlask.ext.database import Box as BoxModel
from projetoFlask.ext.database import db
from projetoFlask.blueprints.webui.services import flashMessagesService


@login_required
def myBoxes():
    boxes = BoxModel.query.filter_by(deleted=False).order_by(BoxModel.name)
    return render_template("boxes/index.html", items=boxes)

@login_required
def newBox():
    form = BoxCreate(request.form)

    if request.method == 'POST' and form.validate():
        box = BoxModel(
          name=form.name.data,
          goal=form.goal.data,
          value=0,
          description=form.description.data,
          user=current_user
        )
        
        try:
          box.persist()
          flashMessagesService.addSuccessMessage("A caixinha foi criada com sucesso!")
          return redirect(url_for('webui.myBoxes'))
        except:
          flashMessagesService.addErrorMessage("Ocorreu um erro ao tentar salvar a caixinha.")
          
    return render_template("boxes/new.html", form=form, box=BoxModel())

def editBox(id):
    form = BoxCreate(request.form)
    box = db.get_or_404(BoxModel, id)
      
    if request.method == 'POST':
        try:
            box.name=form.name.data
            box.goal=form.goal.data
            box.description=form.description.data

            box.persist()

            flashMessagesService.addSuccessMessage("A caixinha foi editada com sucesso!")
            return redirect(url_for('webui.myBoxes'))
        except:
            flashMessagesService.addErrorMessage("Ocorreu um erro ao tentar salvar a caixinha.")
          
    return render_template("boxes/edit.html", form=form, box=box)


def deleteBox(id):
    box = db.get_or_404(BoxModel, id)
      
    if box.value > 0:
        flashMessagesService.addErrorMessage("A caixinha contém saldo. Por isso, não pode ser deletada.")
        return redirect(url_for('webui.myBoxes'))

    try:
        box.remove()
        flashMessagesService.addSuccessMessage("A caixinha foi deletada com sucesso!")
    except:
        flashMessagesService.addErrorMessage("Ocorreu um erro ao tentar deletar a caixinha.")
          
    return redirect(url_for('webui.myBoxes'))

