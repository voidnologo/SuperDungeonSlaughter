from src.models.combatant import Combatant


class CombatEngine:
    """Manages combat interactions between combatants."""

    @staticmethod
    def execute_attack(attacker: Combatant, defender: Combatant) -> None:
        """Execute an attack from attacker to defender."""
        attacker.attack(defender)

    @staticmethod
    def is_defeated(combatant: Combatant) -> bool:
        """Check if combatant has been defeated (HP <= 0)."""
        return combatant.hp <= 0
