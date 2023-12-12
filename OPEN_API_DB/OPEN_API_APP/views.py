
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .models import PDF_fields, PDF_pathfiles
from OPEN_API_APP.serializers import PDF_Serializer
from rest_framework.parsers import MultiPartParser, FormParser
from .sample import PDFProcessor, db_config, table_name
import os


class OpenApITextExtractionAPI(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = PDF_Serializer

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('pdf')
        pdf_paths = []

        for file in files:
            data = {'pdf': file}
            serializer = PDF_Serializer(data=data)
            if serializer.is_valid():
                saved_instance = serializer.save()
                pdf_paths.append(saved_instance.pdf.path)

        # Instantiate PDFProcessor with db_config
        pdf_processor = PDFProcessor()

        # Call extract_and_generate_information method
        result = pdf_processor.extract_and_generate_information(pdf_paths)


        for file_path in pdf_paths:
            os.remove(file_path)

        return Response({"pdf_paths": pdf_paths, "result": result})
