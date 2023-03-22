from flask import render_template, request, redirect, url_for, abort
from projetoFlask.blueprints.webui.forms.BoxForm import BoxCreate
from flask_login import login_required, current_user
from projetoFlask.ext.database import Box as BoxModel
from projetoFlask.blueprints.webui.services import flashMessagesService
from projetoFlask.blueprints.webui.repository.BoxRepository import BoxRepository


@login_required
def myBoxes():
    page = request.args.get('page', 1, type=int)
    pagination = BoxRepository.findMyActivesBoxes(current_user).paginate(page=page, per_page=10, error_out=False)

    return render_template("boxes/index.html", pagination=pagination)

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
    box = BoxRepository.findOneActiveBox(id=id, current_user=current_user)

    if not box:
        flashMessagesService.addWarningMessage("Não encontramos sua caixinha.")
        return redirect(url_for('webui.myBoxes'))
    
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
    box = BoxRepository.findOneActiveBox(id=id, current_user=current_user)

    if not box:
        flashMessagesService.addWarningMessage("Não encontramos sua caixinha.")
        return redirect(url_for('webui.myBoxes'))

    if box.value > 0:
        flashMessagesService.addErrorMessage("A caixinha contém saldo. Por isso, não pode ser deletada.")
        return redirect(url_for('webui.myBoxes'))

    try:
        box.remove()
        flashMessagesService.addSuccessMessage("A caixinha foi deletada com sucesso!")
    except:
        flashMessagesService.addErrorMessage("Ocorreu um erro ao tentar deletar a caixinha.")
          
    return redirect(url_for('webui.myBoxes'))

