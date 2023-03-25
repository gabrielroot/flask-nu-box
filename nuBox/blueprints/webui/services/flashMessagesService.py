from flask import flash


def addSuccessMessage(message):
    flash(message, 'success')


def addWarningMessage(message):
    flash(message, 'warning')


def addInfoMessage(message):
    flash(message, 'info')


def addErrorMessage(message):
    flash(message, 'danger')
