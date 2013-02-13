# coding: utf-8

from django.forms.models import inlineformset_factory

from auf.django.references import models as ref

from cartographie.formation.models import Acces, Formation, \
                                          FormationComposante, \
                                          EtablissementComposante, \
                                          EtablissementAutre

from cartographie.formation.forms.formation import FormationForm


class ModifierViewModel(object):
    token = None
    acces = None
    etablissement = None
    formation = None
    form = None

    composanteFormset = None
    partenaireAufFormset = None
    partenaireAutreFormset = None

    def __init__(self, request, token, formation_id):
        if token:
            self.token = token
            self.acces = Acces.objects.get(token=token)
            self.etablissement = self.acces.etablissement
            self.formation = Formation.objects.get(id=formation_id)

            if request.method == "POST":
                form = FormationForm(
                    self.etablissement,
                    request.POST,
                    instance=self.formation
                )
            else:
                form = FormationForm(
                    self.etablissement,
                    instance=self.formation
                )

            self.form = form

    def set_formsets(self):
        formset = inlineformset_factory(
            Formation,
            FormationComposante,
            exclude=("id", "formation")
        )
        self.composanteFormset = formset(instance=self.formation)

        # self.partenaireAufFormset = inlineformset_factory(
        #     FormationPartenaireAufForm
        # )
        # self.partenaireAutreFormset = inlineformset_factory(
        #     FormationPartenaireAutreForm
        # )

    def get_data(self):
        return {
            "token": self.token,
            "etablissement": self.etablissement,
            "form": self.form,
            "formation": self.formation,
            "composanteFormset": self.composanteFormset,
            "partenaireAufFormset": self.partenaireAufFormset,
            "partenaireAutreFormset": self.partenaireAutreFormset
        }
