# https://www.codewars.com/kata/papers-please/train/python
from typing import Dict, List, Tuple

class Inspector():
    def __init__(self) -> None:
        self.state_dict: Dict = {}

    def receive_bulletin(self, bulletin: str) -> None:
        """
        Updates to the list of nations (comma-separated if more than one) whose citizens may enter (begins empty, before the first bulletin):
            example 1: Allow citizens of Obristan
            example 2: Deny citizens of Kolechia, Republia
        Updates to required documents
            example 1: Foreigners require access permit
            example 2: Citizens of Arstotzka require ID card
            example 3: Workers require work pass
        Updates to required vaccinations
            example 1: Citizens of Antegria, Republia, Obristan require polio vaccination
            example 2: Entrants no longer require tetanus vaccination
        Update to a currently wanted criminal
            example 1: Wanted by the State: Hubert Popovic
        """
        instructions: List = self._parse_bulletin(bulletin)
        for instruction in instructions:
            # Updates to the list of nations:
            if instruction.startswith('Allow citiens') or \
               instruction.startswith('Deny citizens'):
                self._update_list_of_nations(instruction)
            # Update to a currently wanted criminal:
            elif instruction.startswith('Wanted by the state:'):
                self._update_wanted_by_the_state(instruction)
            # Updated to required vaccinations:
            elif 'vaccination' in instruction:
                self._update_required_vaccinations(instruction)
            # Updated to required documents:
            elif 'require' in instruction:
                self._update_required_documents(instruction)
            else:
                raise LookupError(f'Unexpected input: {instruction}')

    def inspect(self, input_entrant: Dict) -> None:
        entrant: Dict = {key.strip():self._str_to_dict(value)
                         for key, value  in input_entrant.items()}

        checks = {}
        checks['required_docs'] = self._check_required_docs(entrant)
        checks['no_conflicting_info'] = self._check_no_conflicting_info(entrant)
        checks['all_docs_current'] = self._check_all_docs_current(entrant)
        checks['not_wanted_criminal'] = self._check_not_wanted_criminal(entrant)
        checks['has_cert_of_vaccination'] = self._check_cert_of_vaccination(entrant)
        checks['has_foreigner_paperwork'] = self._check_foreigner_paperwork(entrant)

        for check, (pass_, reason) in checks.items():
            if not pass_:
                self._fail(entrant, check=check, reason=reason)
                break
        else:
            self._pass(entrant)

    def _pass(self, entrant: Dict) -> str:
        if entrant['citizen']:
            return 'Glory to Arstotzka.'
        else:
            return 'Cause no trouble.'

    def _fail(self, entrant: Dict, check: str, reason: str) -> str:
        return reason

    @staticmethod
    def _str_to_dict(str_dict: str) -> Dict:
        split_string = (elem.split(': ') for elem in str_dict.strip().split('\n'))
        return {key.strip():value.strip() for key, value in split_string}

    @staticmethod
    def _parse_bulletin(bulletin: str) ->  List:
        return bulletin.strip().split('\n')

    @staticmethod
    def _update_list_of_nations(instruction: str) -> None:
        raise NotImplementedError(f'Can\'t hanle input: {instruction}')

    @staticmethod
    def _update_wanted_by_the_state(instruction: str) -> None:
        raise NotImplementedError(f'Can\'t hanle input: {instruction}')

    @staticmethod
    def _update_required_vaccinations(instruction: str) -> None:
        raise NotImplementedError(f'Can\'t hanle input: {instruction}')

    @staticmethod
    def _update_required_documents(instruction: str) -> None:
        raise NotImplementedError(f'Can\'t hanle input: {instruction}')

    def _check_required_docs(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_required_docs yet')

    def _check_no_conflicting_info(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_no_conflicting_info yet')

    def _check_all_docs_current(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_all_docs_current yet')

    def _check_not_wanted_criminal(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_not_wanted_criminal yet')

    def _check_cert_of_vaccination(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_cert_of_vaccination yet')

    def _check_foreigner_paperwork(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_foreigner_paperwork yet')

if __name__ == '__main__':

    entrant1 = {
        "passport": """ID#: GC07D-FU8AR
        NATION: Arstotzka
        NAME: Guyovich, Russian
        DOB: 1933.11.28
        SEX: M
        ISS: East Grestin
        EXP: 1983.07.10"""
    }

    inspector = Inspector()
    inspector.inspect(entrant1)
