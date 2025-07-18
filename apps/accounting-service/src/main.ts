// main.ts
import './tracing';
import { NestFactory } from '@nestjs/core';
import { ValidationPipe, VersioningType } from '@nestjs/common';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';
import helmet from 'helmet';
import { WinstonModule } from 'nest-winston';
import * as winston from 'winston';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';
import { getKafkaConfig } from '../../../packages/shared/events/kafka-config'; // Import shared Kafka config
import { ConfigService } from '@nestjs/config'; // Added import for ConfigService

async function bootstrap() {
  // Configure Winston logger
  const logger = WinstonModule.createLogger({
    transports: [
      new winston.transports.Console({
        format: winston.format.combine(
          winston.format.timestamp(),
          winston.format.colorize(),
          winston.format.printf(({ timestamp, level, message }) => {
            return `${timestamp} [${level}]: ${message}`;
          }),
        ),
      }),
      new winston.transports.File({ 
        filename: 'logs/error.log', 
        level: 'error',
        format: winston.format.combine(
          winston.format.timestamp(),
          winston.format.json(),
        ),
      }),
      new winston.transports.File({ 
        filename: 'logs/combined.log',
        format: winston.format.combine(
          winston.format.timestamp(),
          winston.format.json(),
        ),
      }),
    ],
  });

  // 1) Crée l'application à partir de AppModule
  const app = await NestFactory.create(AppModule, { logger });
  const configService = app.get(ConfigService);

  // Configure and connect Kafka consumer for accounting-service
  const kafkaConsumerOptions = getKafkaConfig(configService); // Get base config
  app.connectMicroservice<MicroserviceOptions>({
    ...kafkaConsumerOptions, // Spread base config (transport and options)
    options: {
      ...kafkaConsumerOptions.options!,
      client: {
        ...kafkaConsumerOptions.options!.client!,
        clientId: 'accounting-service-consumer', // Specific client ID
      },
      consumer: {
        ...kafkaConsumerOptions.options!.consumer!,
        groupId: 'accounting-consumer-group', // Specific consumer group ID
      },
    },
  });

  // Start all microservices
  await app.startAllMicroservices();
  
  // 2) Enable versioning
  app.enableVersioning({
    type: VersioningType.URI,
    defaultVersion: '1',
  });

  // 3) Security middleware
  app.use(helmet());
  
  // 4) CORS configuration
  app.enableCors({
    origin: [
      'http://localhost:3000',
      'http://localhost:3001',
      'http://localhost:3002',
      'http://localhost:3003',
    ],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'Accept'],
    exposedHeaders: ['Authorization'],
    credentials: true,
    maxAge: 3600,
  });
  
  // 5) Global validation pipe
  app.useGlobalPipes(new ValidationPipe({
    transform: true,
    whitelist: true,
    forbidNonWhitelisted: true,
    validationError: { target: false },
  }));

  // 6) Swagger documentation setup
  const config = new DocumentBuilder()
    .setTitle('Kiota Accounting Service API')
    .setDescription('The Kiota Accounting Service API documentation')
    .setVersion('1.0')
    .addBearerAuth()
    .addTag('accounts')
    .addTag('journals')
    .addTag('reports')
    .addTag('treasury')
    .addTag('taxes')
    .addTag('chat')
    .addTag('health')
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, document);

  // 7) Démarre l'app sur le port 3003
  await app.listen(3003);

  // ➜ TON endpoint `/metrics` se trouvera sur http://localhost:3003/metrics
  //    Parce que dans AppModule -> MonitoringModule -> PrometheusController
}
bootstrap();
