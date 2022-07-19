from itertools import zip_longest


class CalcularRede:
    def __init__(self, ip_cidr: str):
        self.ip = ip_cidr

        try:
            self._aferindo_range()

        except Exception as erro:
            print(erro)

        else:
            print(f'Endereço/Rede: {self.ip}')
            print(f'Endereço IP: {self._removendo_barra()[0]}')
            print(f'Prefixo CIDR: /{self._get_mask()}')
            print(f'A Máscara da Sub-Rede é {self._mask_sub_rede()}')
            print(f'IP da Rede: {self._ip_rede()}/{self._get_mask()}')
            print(f'Broadcast da Rede: {self._broadcast_rede()}')
            print(f'Primeiro Host: {self._ip_primeiro_host()}')
            print(f'Último Host: {self._ip_ultimo_host()}')
            print(f'Total de IPs para uso: {self._total_hosts()}')
    # _____________________________________________

    def _removendo_barra(self) -> list:  # Separa o IP da Máscara
        return [x for x in self.ip.split('/')]
    # _____________________________________________

    def _removendo_ponto(self) -> list:  # Pega o IP e separa por pontos em 4 ‘strings’ diferentes
        return [x for x in self._removendo_barra()[0].split('.')]
    # _____________________________________________

    def _get_mask(self) -> int:  # transforma em int a máscara
        return int(self._removendo_barra()[1])
    # _____________________________________________

    def _get_ip(self) -> list:  # Transforma em int a lista removendo_ponto()
        return [int(x) for x in self._removendo_ponto()]
    # _____________________________________________

    def _aferindo_range(self):  # Tenta rodar as duas funções e conferindo a amplitude dos números
        try:
            self._get_ip()
            self._get_mask()

        except Exception:
            raise ValueError("IP inválido, use o formato 255.255.255.255/32")

        else:
            for x in self._get_ip():
                if x < 0 or x > 255:
                    raise TypeError('O IP tem que estar entre 0-255')

            if self._get_mask() < 0 or self._get_mask() > 32:
                raise TypeError('A Máscara tem que estar entre 0-32')
    # _____________________________________________

    def _get_ip_binario(self) -> list:  # Retorna a lista de IP em formato binário
        return ['{:0>8}'.format(f'{x:b}') for x in self._get_ip()]
    # _____________________________________________

    def _juntar_ip_binario(self) -> str:  # Junta as 4 ‘strings’ do IP em uma só
        return ''.join(self._get_ip_binario())
    # _____________________________________________

    def _bits_host(self) -> int:  # Quantos bits sobraram para os Hosts usarem
        return 32 - self._get_mask()  # 32 é a quantidade total de caracteres no IP binário
    # _____________________________________________

    def _total_hosts(self) -> int:  # Número total de dispositivos possíveis na rede
        return (2 ** self._bits_host()) - 2
    # _____________________________________________

    def _repete_1_tamanho_mascara(self) -> str:
        return '1' * self._get_mask()
    # _____________________________________________

    def _completar_ip(self, str_ip_incompleto: str, numero: str) -> list:  # Pega o IP binário e preenche o incompleto
        original_e_preenchido = zip_longest(str(self._juntar_ip_binario()), str_ip_incompleto, fillvalue=numero)
        return list(original_e_preenchido)  # Retorna uma lista com tuplas dentro
    # _____________________________________________

    def _get_ip_till_bits_host(self) -> str:  # Pega o IP binário menos a quantidade de bit pro host
        return self._juntar_ip_binario()[:- self._bits_host()]
    # _____________________________________________

    def _setting_mask_sub_rede(self) -> list:  # Retorna uma lista com tuplas dentro
        return self._completar_ip(self._repete_1_tamanho_mascara(), '0')
    # _____________________________________________

    def _setting_ip_rede(self) -> list:
        return self._completar_ip(self._get_ip_till_bits_host(), '0')
    # _____________________________________________

    def _setting_ip_broadcast(self) -> list:
        return self._completar_ip(self._get_ip_till_bits_host(), '1')
    # _____________________________________________

    @staticmethod
    def _separar_ip_binario(local) -> list:
        final = []
        auxiliar = []
        for _, y in local:
            auxiliar.append(y)

            if len(auxiliar) == 8:
                final.append(auxiliar)
                auxiliar = []
        return final
    # _____________________________________________

    def _get_ip_lista(self, local) -> list:  # Junta numa lista o IP binário no formato de ‘string’
        ip_quase_junto = self._separar_ip_binario(local)
        ip_junto = []
        for x in ip_quase_junto:
            ip_junto.append(''.join(x))
        return ip_junto
    # _____________________________________________

    def _get_ip_rede(self) -> list:  # Lista do IP binário da Rede
        return self._get_ip_lista(self._setting_ip_rede())
    # _____________________________________________

    def _get_ip_broadcast(self) -> list:  # Lista do IP binário do Broadcast
        return self._get_ip_lista(self._setting_ip_broadcast())
    # _____________________________________________

    def _get_sub_mask_ip(self) -> list:  # Retorna uma lista com o IP em 4 ‘strings’
        return self._get_ip_lista(self._setting_mask_sub_rede())
    # _____________________________________________

    @staticmethod
    def _conv_bi_num(local: list) -> list:  # Converte de Binário para Numérico
        convertido = []
        for binario in local:
            convertido.append(str(int(binario, 2)))
        return convertido
    # _____________________________________________

    def _conv_rede(self) -> list:  # Converte o IP binário em numérico
        return self._conv_bi_num(self._get_ip_rede())
    # _____________________________________________

    def _conv_broadcast(self) -> list:  # Converte o IP binário em numérico
        return self._conv_bi_num(self._get_ip_broadcast())
    # _____________________________________________

    def _conv_sub_mask(self) -> list:  # Converte para numérico a sub-rede
        return self._conv_bi_num(self._get_sub_mask_ip())
    # _____________________________________________

    def _broadcast_rede(self) -> str:  # Junta o Broadcast da Rede
        return '.'.join(self._conv_broadcast())
    # _____________________________________________

    def _mask_sub_rede(self) -> str:  # Junta a sub-rede convertida
        return '.'.join(self._conv_sub_mask())
    # _____________________________________________

    def _ip_rede(self) -> str:  # Junta o IP convertido
        return '.'.join(self._conv_rede())
    # _____________________________________________

    def _primeiro_host(self) -> str:  # Retorna o primeiro IP disponível
        return str(int(self._conv_rede()[-1]) + 1)
    # _____________________________________________

    def _ultimo_host(self) -> str:  # Retorna o último IP dispinível
        return str(int(self._conv_broadcast()[-1]) - 1)
    # _____________________________________________

    def _ip_primeiro_host(self) -> str:  # Junta o IP
        primeiros = [x for x in self._conv_rede()[:3]]
        ultimo = self._primeiro_host()
        primeiros.append(ultimo)
        return '.'.join(primeiros)
    # _____________________________________________

    def _ip_ultimo_host(self) -> str:  # Junta o IP
        primeiros = [x for x in self._conv_broadcast()[:3]]
        ultimo = self._ultimo_host()
        primeiros.append(ultimo)
        return '.'.join(primeiros)
