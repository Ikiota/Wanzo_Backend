
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne } from 'typeorm';
import { Company, LocationType } from './company.entity';

@Entity('locations')
export class Location {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  address: string;

  @Column('jsonb')
  coordinates: {
    lat: number;
    lng: number;
  };
  @Column({
    type: 'enum',
    enum: LocationType,
    enumName: 'location_type_enum'
  })
  type: LocationType;

  @ManyToOne(() => Company, company => company.locations)
  company: Company;

  @CreateDateColumn({ name: 'created_at' })
  createdAt: Date;

  @UpdateDateColumn({ name: 'updated_at' })
  updatedAt: Date;
}
