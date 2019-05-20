from unittest import TestCase

from cookbox_scraper.allrecipes import AllRecipes

from . import RecipeScraperTestMixin


class TestMarmitonScraper(RecipeScraperTestMixin, TestCase):
    def setUp(self):
        self.url = 'https://www.marmiton.org/recettes/recette_tarte-aux-brocolis-et-a-la-poudre-d-amandes_23418.aspx'
        self.host = 'marmiton.org'
        self.title = 'Tarte aux brocolis et à la poudre d\'amandes'
        self.description = ''
        self.time = (30, 15, 15)
        self.yield_unit = 'Servings'
        self.yields = (4.0, 1)
        self.ingredients = [('All', [(200.0, None, 'g de pâte brisée'), (500.0, None, 'g de brocoli'), (150.0, None, 'g de crème'), (2.0, None, 'oeufs'), (30.0, None, "g de poudre d'amande"), (30.0, None, 'g de beurre'), (0, None, 'Poivre'), (0, None, 'Sel'), (0, None, 'Muscade')])]
        self.instructions = ['Etape 1 Préchauffez le four à 180°c (thermostat 6)', "Etape 2 Pochez les bouquets de brocolis 2 minutes dans l'eau bouillante puis égouttez", 'Etape 3 Etalez la pâte dans un moule à tarte beurré', ' Disposez les bouquets de brocolis dessus', "Etape 4 Mélangez les oeufs, la crème et la poudre d'amandes", " Assaisonnez de sel, de poivre et d'une pincée de muscade", ' Versez sur les brocolis et parsemez de noisettes de beurre', 'Etape 5 Enfournez pour 50 minutes de cuisson']
        self.notes = []

        super().setUp()
