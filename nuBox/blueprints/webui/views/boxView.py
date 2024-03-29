from flask import request, url_for, redirect, render_template
from flask_login import current_user, login_required

from nuBox.ext.database import Box as BoxModel
from nuBox.blueprints.webui.services import flashMessagesService
from nuBox.blueprints.webui.forms.BoxForm import BoxCreate
from nuBox.blueprints.webui.repository.BoxRepository import BoxRepository


@login_required
def myBoxes():
    page = request.args.get('page', 1, type=int)
    pagination = BoxRepository.findMyActivesBoxes(current_user).\
        paginate(page=page, per_page=10, error_out=False)

    return render_template("boxes/index.html", pagination=pagination)


@login_required
def newBox():
    form = BoxCreate(request.form)

    if request.method == "POST":
        try:
            box = BoxModel(
                name=form.name.data,
                goal=form.goal.data,
                value=0,
                description=form.description.data,
                user=current_user
            )

            if form.goal.data <= 0 or not form.name.data:
                raise ValueError

            box.persist()
            flashMessagesService.\
                addSuccessMessage("A caixinha foi criada com sucesso!")
            return redirect(url_for('webui.myBoxes'))
        except ValueError:
            flashMessagesService.\
                addErrorMessage("A entrada informada é inválida.")
            return render_template("boxes/new.html", form=form, box=box)

    return render_template("boxes/new.html", form=form, box=BoxModel())


@login_required
def editBox(id):
    form = BoxCreate(request.form)
    box = BoxRepository.findOneActiveBox(id=id, current_user=current_user)

    if not box:
        flashMessagesService.addWarningMessage("Não encontramos sua caixinha.")
        return redirect(url_for('webui.myBoxes'))

    try:
        if form.validate_on_submit():
            box.name = form.name.data
            box.goal = form.goal.data
            box.description = form.description.data

            box.persist()

            flashMessagesService.\
                addSuccessMessage("A caixinha foi editada com sucesso!")
            return redirect(url_for('webui.myBoxes'))
        elif request.method == 'POST':
            raise ValueError
    except ValueError:
        flashMessagesService.addErrorMessage("A entrada informada é inválida.")

    return render_template("boxes/edit.html", form=form, box=box)


@login_required
def deleteBox(id):
    box = BoxRepository.findOneActiveBox(id=id, current_user=current_user)

    if not box:
        flashMessagesService.addWarningMessage("Não encontramos sua caixinha.")
        return redirect(url_for('webui.myBoxes'))

    if box.value > 0:
        flashMessagesService.addErrorMessage("A caixinha contém saldo. Por isso, não pode ser deletada.")
        return redirect(url_for('webui.myBoxes'))

    box.remove()
    flashMessagesService.addSuccessMessage("A caixinha foi deletada com sucesso!")

    return redirect(url_for('webui.myBoxes'))
