from datetime import datetime

from django.db import models
from django.conf import settings
from pymongo import ASCENDING, DESCENDING, MongoClient

from user.models import Profile


class Type(models.Model):
    name = models.CharField(
        max_length=45,
        null=False,
        blank=False,
        unique=True,
        help_text='Tipo de discussão.',
    )
    description = models.TextField(
        null=False,
        blank=False,
        help_text='Descrição do tipo de discussão.',
    )

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]

class Theme(models.Model):
    name = models.CharField(
        max_length=45,
        null=False,
        blank=False,
        unique=True,
        help_text='Tema da discussão.',
    )
    type = models.ForeignKey(
        Type,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text='Tipo de discussão à qual pertence',
    )

    class Meta:
        indexes = [
            models.Index(fields=['-name'])
        ]


class ProposalBase:
    theme = models.ForeignKey(
        Theme,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text='Thema da proposta',
    )
    subject = models.CharField(
        max_length=45,
        null=False,
        blank=False,
        unique=True,
        help_text='Assunto pautado para a discussão.',
    )
    proposal = models.TextField(
        null=False,
        blank=False,
        help_text='Proposta para o tema pautado.',
    )
    comments_collection = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        help_text='Collection dos comentátios no Mongo DB',
    )
    sources = models.JSONField(
        null=False,
        blank=False,
        help_text='Json com as fontes da proposta.',
    )
    creation_timestamp = models.FloatField(
        null=False,
        blank=False,
        default=datetime.now().timestamp(),
        help_text='Data de criação da proposta/dicussão.',
    )


class Proposal(ProposalBase, models.Model):
    """
    Propostas que qualquer um pode comentar.
    """
    proposer = models.ForeignKey(
        Profile,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        help_text='Propositor(a).',
    )


class Debate(ProposalBase, models.Model):
    participants = models.ManyToOneRel(
        models.ForeignKey,
        to=Profile,
        field_name='id',
        on_delete=models.CASCADE,
    )


class Comments:
    @staticmethod
    def set_a_comment(profile: Profile, proposal: Proposal, comment: str, sources: list[str]=[]) -> None:
        """
        profile: Objeto Django do usuário que está comentando.
        proposal: Objeto Django da proposta.
        comment:  Comentário
        sources: Fontes
        """
        try:
            _db = MongoClient(
                host=settings.MONGODB['host'],
                port=settings.MONGODB['port'],
            )[settings.MONGODB['db']]
            _collection = _db.get_collection(proposal.comments_collection)
            _collection.insert_one({
                'user': {
                    'id': profile.pk,
                    'name': f'{profile.first_name} {profile.last_name}',
                },
                'comment': comment,
                'sources': sources,
                'timestamp': datetime.now().timestamp(),
            })
            _db.client.close()
        except Exception as e:
            raise e

    @staticmethod
    def get_comments(proposal: Proposal, filter: dict={}) -> tuple[dict]:
        """
        proposal: Objeto Django da proposta.
        filter:  Filtro da consulta.
        """
        try:
            _db = MongoClient(
                host=settings.MONGODB['host'],
                port=settings.MONGODB['port'],
            )[settings.MONGODB['db']]
            _collection = _db.get_collection(proposal.comments_collection)
            _result = _collection.find(filter)\
                .limit(100)\
                .sort({ '_id': ASCENDING })
            _result = tuple(_result)
            _db.client.close()

            return tuple(_result)
        except Exception as e:
            raise e

    @staticmethod
    def count_comments(proposal: Proposal) -> int:
        """
        proposal: Objeto Django da proposta.
        """
        try:
            _db = MongoClient(
                host=settings.MONGODB['host'],
                port=settings.MONGODB['port'],
            )[settings.MONGODB['db']]
            _collection = _db.get_collection(proposal.comments_collection)
            _result = _collection.count_documents()
            _db.client.close()

            return _result
        except Exception as e:
            raise e

    @staticmethod
    def init_comments(proposal: Proposal) -> None:
        try:
            _db = MongoClient(
                host=settings.MONGODB['host'],
                port=settings.MONGODB['port'],
            )[settings.MONGODB['db']]
            _collection = _db.get_collection(proposal.comments_collection)
            _collection.create_index([
                ('user.id', DESCENDING),
                ('timestamp', ASCENDING)
            ])
            _db.client.close()
        except Exception as e:
            raise e
