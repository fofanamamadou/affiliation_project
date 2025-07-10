from django.core.management.base import BaseCommand
from remise.models import Remise
from decimal import Decimal


class Command(BaseCommand):
    help = 'Calcule automatiquement les remises pour tous les influenceurs ayant des prospects confirmés'

    def add_arguments(self, parser):
        parser.add_argument(
            '--montant-par-prospect',
            type=float,
            default=1000,
            help='Montant en euros par prospect confirmé (défaut: 1000FCFA)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui serait fait sans effectuer les changements'
        )

    def handle(self, *args, **options):
        montant_par_prospect = Decimal(str(options['montant_par_prospect']))
        dry_run = options['dry_run']

        self.stdout.write(
            self.style.SUCCESS(f'Calcul des remises automatiques (montant par prospect: {montant_par_prospect}FCFA)')
        )

        if dry_run:
            self.stdout.write(self.style.WARNING('Mode DRY RUN - Aucun changement ne sera effectué'))

        try:
            remises_creees = Remise.generer_remises_pour_tous(montant_par_prospect)
            
            if remises_creees:
                self.stdout.write(
                    self.style.SUCCESS(f'{len(remises_creees)} remise(s) créée(s) automatiquement')
                
                for remise in remises_creees:
                    self.stdout.write(
                        f'  - {remise.influenceur.nom}: {remise.montant}FCFA ({remise.description})'
                    )
            else:
                self.stdout.write(
                    self.style.WARNING('Aucune remise à créer. Tous les prospects confirmés ont déjà une remise.')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors du calcul des remises : {str(e)}')
            ) 