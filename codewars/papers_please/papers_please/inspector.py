# https://www.codewars.com/kata/papers-please/train/python
from typing import Dict, List, Tuple, Union
import datetime

class Inspector():
    def __init__(self, state_dict: Union[Dict, None] = None) -> None:
        if state_dict:
            self.state_dict = state_dict
        else:
            self.state_dict: Dict = {
                'allowed_countries': [],
                'denied_countries': [],

            }

    def __repr__(self) -> str:
        return f'Inspector({self.state_dict})'

    def receive_bulletin(self, bulletin: str) -> None:
        """
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
            if instruction.startswith('Allow citizens') or \
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

    def inspect(self, input_entrant: Dict) -> str:
        entrant: Dict = {key.strip():self._str_to_dict(value)
                         for key, value  in input_entrant.items()}

        checks = {}
        checks['denied_countries'] = self._check_denied_countries(entrant)
        checks['all_docs_current'] = self._check_all_docs_current(entrant)
        try:
            # TODO:
            checks['required_docs'] = self._check_required_docs(entrant)
            checks['no_conflicting_info'] = self._check_no_conflicting_info(entrant)
            checks['all_docs_current'] = self._check_all_docs_current(entrant)
            checks['not_wanted_criminal'] = self._check_not_wanted_criminal(entrant)
            checks['has_cert_of_vaccination'] = self._check_cert_of_vaccination(entrant)
            checks['has_foreigner_paperwork'] = self._check_foreigner_paperwork(entrant)
        except:
            pass

        for check, (pass_, reason) in checks.items():
            if not pass_:
                return self._fail(entrant, check=check, reason=reason)
        else:
            return self._pass(entrant)

    def _pass(self, entrant: Dict) -> str:
        if entrant.get('citizen', False):
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
        return [instruction.strip() for instruction in bulletin.strip().split('\n')]

    def _update_list_of_nations(self, instruction: str) -> None:
        """Updates to the list of nations (comma-separated if more than one) whose citizens
        may enter (begins empty, before the first bulletin):
        example 1: Allow citizens of Obristan
        example 2: Deny citizens of Kolechia, Republia
        """
        if instruction.startswith('Allow citizens'):
            allowed_countries = instruction[len('Allow citizens of '):].split(',')
            self.state_dict['allowed_countries'].extend(
                [country.strip().capitalize() for country in allowed_countries])
            self.state_dict['denied_countries'] = [country for country in
                self.state_dict['denied_countries'] if country not in allowed_countries]
        elif instruction.startswith('Deny citizens'):
            denied_countries = instruction[len('Deny citizens of '):].split(',')
            self.state_dict['denied_countries'].extend(
                [country.strip().capitalize() for country in denied_countries])
            self.state_dict['allowed_countries'] = [country for country in
                self.state_dict['allowed_countries'] if country not in denied_countries]
        else:
            raise NotImplementedError(f'Can\'t handle input: {instruction}')


    def _update_wanted_by_the_state(self, instruction: str) -> None:
        raise NotImplementedError(f'Can\'t handle input: {instruction}')

    def _update_required_vaccinations(self, instruction: str) -> None:
        raise NotImplementedError(f'Can\'t handle input: {instruction}')

    def _update_required_documents(self, instruction: str) -> None:
        raise NotImplementedError(f'Can\'t handle input: {instruction}')

    def _check_denied_countries(self, entrant: Dict) -> Tuple[bool, str]:
        if entrant.get('passport', {}).get('NATION') in self.state_dict['denied_countries']:
            return False, f'Entry denied: {entrant.get("passport", {}).get("NATION", None)} in list of denied countries'
        else:
            return True, ''

    def _check_required_docs(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_required_docs yet')

    def _check_no_conflicting_info(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_no_conflicting_info yet')

    def _check_all_docs_current(self, entrant: Dict) -> Tuple[bool, str]:
        for doc, doc_fields in entrant.items():
            if doc_fields.get('EXP'):
                # Hard coded date November 22, 1982
                # Date format 1: 1983.07.10
                date = datetime.datetime.strptime(doc_fields['EXP'], '%Y.%m.%d')
                if date <= datetime.datetime.strptime('1982.11.22', '%Y.%m.%d'):
                    return False, f'Entry denied: {doc} expired'
        else:
            return True, ''

    def _check_not_wanted_criminal(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_not_wanted_criminal yet')

    def _check_cert_of_vaccination(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_cert_of_vaccination yet')

    def _check_foreigner_paperwork(self, entrant: Dict) -> Tuple[bool, str]:
        raise NotImplementedError(f'Unable to perform check_foreigner_paperwork yet')

if __name__ == '__main__':

    i = Inspector()
    bulletin1 = """Deny citizens of Russia
               Allow citizens of Belarus
               """
    i.receive_bulletin(bulletin1)

    entrant1 = {
        "passport": """ID#: GC07D-FU8AR
        NATION: Arstotzka
        NAME: Guyovich, Russian
        DOB: 1933.11.28
        SEX: M
        ISS: East Grestin
        EXP: 1983.07.10"""
    }

    entrant2 = {
        "passport": """ID#: GC07D-FU8AR
        NATION: Russia
        NAME: Guyovich, Russian
        DOB: 1933.11.28
        SEX: M
        ISS: East Grestin
        EXP: 1983.07.10"""
    }

    entrant3 = {
        "passport": """ID#: GC07D-FU8AR
        NATION: Arstotzka
        NAME: Guyovich, Russian
        DOB: 1933.11.28
        SEX: M
        ISS: East Grestin
        EXP: 1980.07.10"""
    }

    i.receive_bulletin("""Deny citizens of Belarus
                        Allow citizens of Albania""")
